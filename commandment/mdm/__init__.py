"""mdm app module: Controller logic for MDM Blueprint"""

import sys
import os
import plistlib
import xml.parsers.expat

from functools import wraps
from M2Crypto import SMIME, BIO, X509
from flask import current_app, request, g, abort, make_response, send_file
from sqlalchemy.sql.expression import true

from . import enroll
from ..pki.x509 import Certificate
from ..database import db_session, NoResultFound, or_, and_
from ..mdmcmds import InstallProfile, AppInstall, UpdateInventoryDevInfoCommand, find_mdm_command_class
from ..profiles.mdm import MDMPayload
from ..mdmcmds.dep import DeviceConfigured
from ..models import App, app_group_assoc, SCEPConfig, Device, Certificate as DBCertificate, MDMGroup, MDMConfig, QueuedCommand
from ..pki.ca import get_ca, PushCertificate
from ..push import push_to_device
from ..profiles import Profile
from ..profiles.cert import PKCS12CertificatePayload, PEMCertificatePayload, SCEPPayload

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'
TRUST_DEV_PROVIDED_CERT = True

def base64_to_pem(crypto_type, b64_text, width=76):
    """Convert a base64 device response to a PEM."""
    lines = ''
    for pos in xrange(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)

def plist_from_pkcs7(pkcs7):
    """Extract a plist from PKCS7 encoded data."""
    # DEP request

    # base64 encode the DER data, and wrap in a PEM-ish format for SMIME.load_pkcs7_bio()
    req_data = base64_to_pem('PKCS7', pkcs7)

    p7_bio = BIO.MemoryBuffer(str(req_data))
    pkcs7 = SMIME.load_pkcs7_bio(p7_bio)

    p7_signers = pkcs7.get0_signers(X509.X509_Stack())

    signer = SMIME.SMIME()
    signer.set_x509_store(X509.X509_Store())
    signer.set_x509_stack(p7_signers)

    # TODO/XXX: not verifying ANY certificates!
    #
    # spec says we should verify against the "Apple Root CA" and that this
    # CMS message contains all intermediates to do that verification.
    # M2Crypto has no way to get at all the intermediate certificates to
    # do this manually we'd need to extract all of the certificates and
    # verify the chain aginst it. Note as of 2016-03-14 on a brand new
    # iPad Apple was including an expired certificate in this chain. Note
    # also that at least one of the intermediate certificates had a
    # certificate purpose apparently not appropraite for CMS/SMIME
    # verification. For now just verify with no CA and skip any
    # verification.
    plist_text = signer.verify(pkcs7, None, flags=SMIME.PKCS7_NOVERIFY)

    plist = plistlib.readPlistFromString(plist_text)

    return plist

def do_enroll(pks7):
    """Enroll a device from the pks7 data it sent."""

    current_app.logger.info("ENROLL")
    plist = plist_from_pkcs7(pks7)

    device = enroll.enroll_from_plist(plist)

    return device


def verify_mdm_signature(mdm_sig, req_data):
    """Verify the client's supplied MDM signature and return the client certificate included in the signature."""

    p7_bio = BIO.MemoryBuffer(str(mdm_sig))
    pkcs7 = SMIME.load_pkcs7_bio(p7_bio)

    p7_signers = pkcs7.get0_signers(X509.X509_Stack())

    mdm_ca = get_ca()

    # can probably directly use m2 certificate here
    ca_x509_bio = BIO.MemoryBuffer(mdm_ca.get_cacert().to_pem())
    ca_x509 = X509.load_cert_bio(ca_x509_bio)

    cert_store = X509.X509_Store()
    cert_store.add_x509(ca_x509)

    signer = SMIME.SMIME()
    signer.set_x509_store(cert_store)
    signer.set_x509_stack(p7_signers)

    # NOTE: may need to do something special if we can't cleanly convert
    # to string from Unicode. must be byte-accurate as the signature won't
    # match otherwise
    data_bio = BIO.MemoryBuffer(req_data)

    # will raise an exception if verification fails
    # if no CA certificate we get an:
    #   PKCS7_Error: certificate verify error
    signer.verify(pkcs7, data_bio)

    return p7_signers[0].as_pem()

def device_cert_check(no_device_okay=False):
    """Performs a set of checks on a request to make sure it came from a
    legimately enrolled device in this MDM system"""
    def decorator(func):
        """Decorator for checking certs prior to request handler."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Actual wrapper the we give to the request handler."""
            # check if valid certificate and if request data matches signature
            # TODO: implement alternate methods of getting supplied client cert
            # (e.g. request.headers['X-Ssl-Client-Cert'].replace('\n ', '\n') for 
            # nginx)
            pkcs7_pem_sig = base64_to_pem('PKCS7', request.headers['Mdm-Signature'])
            device_supplied_cert = verify_mdm_signature(pkcs7_pem_sig, request.data)

            try:
                dev_cert_fprint = Certificate.from_pem(device_supplied_cert).get_fingerprint()
                g.device_cert = db_session.query(DBCertificate).filter(DBCertificate.fingerprint == dev_cert_fprint).one()
            except NoResultFound:
                current_app.logger.info('supplied device certificate not found; returning invalid')
                abort(400, 'certificate invalid')

            # get a list of the devices that correspond to this certificate
            cert_devices = g.device_cert.devices

            if len(cert_devices) > 1:
                dev_id_list = ', '.join([i.id for i in cert_devices])
                current_app.logger.info('certificate has more than one device assigned (%s); returning invalid' % dev_id_list)
                abort(500, 'certificate configuration invalid')
            elif len(cert_devices) < 1 and no_device_okay is not True:
                current_app.logger.info('certificate has no associated device; returning invalid')
                abort(400, 'certificate invalid')

            # NOTE: we've seen on odd circumstance where the provided device UDID
            # does not match the currently enrolled certificate (and thus device
            # UDID). this appears to be some weird certificate caching problem
            # on the client side there the client tries to auth with it's
            # previously enrolled cert when one removes/re-enrolls a device
            # quickly
            if len(cert_devices) == 1:
                g.device = g.device_cert.devices[0]
            else:
                g.device = None

            return func(*args, **kwargs)
        return wrapper
    return decorator

def parse_plist_input_data(func):
    """Parses plist data as HTTP input from request"""
    @wraps(func)
    def decorator(*args, **kwargs):
        """Decorator for parsing HTTP input into a plist"""
        try:
            g.plist_data = plistlib.readPlistFromString(request.data)
        except xml.parsers.expat.ExpatError:
            current_app.logger.info('could not parse property list input data')
            abort(400, 'invalid input data')

        return func(*args, **kwargs)
    return decorator

def device_first_post_enroll(device, awaiting=False):
    """Get device information after enrolment"""
    print 'enroll:', 'UpdateInventoryDevInfoCommand'
    db_session.add(UpdateInventoryDevInfoCommand.new_queued_command(device))

    # install all group profiles
    for group in device.mdm_groups:
        for profile in group.profiles:
            print "Installing profile ", profile.id
            db_session.add(InstallProfile.new_queued_command(device, {'id': profile.id}))

    if awaiting:
        # in DEP Await state, send DeviceConfigured to proceed with setup
        db_session.add(DeviceConfigured.new_queued_command(device))

    db_session.commit()

    push_to_device(device)

def device_first_user_message(device):
    """Queue the MDM commands appropriate for a first-user-message seen
    event. Currently used to inititate DEP app installations."""

    device.first_user_message_seen = True

    for group in device.mdm_groups:
        app_q = db_session.query(App).join(
            app_group_assoc,
            and_(app_group_assoc.c.mdm_group_id == group.id, app_group_assoc.c.app_id == App.id)
        ).filter(
            app_group_assoc.c.install_early == true()
        )

        for app in app_q:
            db_session.add(AppInstall.new_queued_command(device, {'id': app.id}))

    db_session.commit()

    push_to_device(device)

def get_webcrts(config):
    """Find and include all mdm.webcrt's"""

    query = db_session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.webcrt')
    webcrt_profiles = []
    for i, cert in enumerate(query):
        new_webcrt_profile = PEMCertificatePayload(config.prefix + '.webcrt.%d' % i, str(cert.pem_certificate).strip(), PayloadDisplayName='Web Server Certificate')
        webcrt_profiles.append(new_webcrt_profile)
    return webcrt_profiles

def generate_mdm_payload():
    """Get a payload with the necessary information about the MDM"""
    mdm_ca = get_ca()

    config = db_session.query(MDMConfig).first()

    if not config:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    if not config.prefix or not config.prefix.strip():
        abort(500, 'MDM configuration has no profile prefix')

    profile = Profile(config.prefix + '.enroll', PayloadDisplayName=config.mdm_name)

    ca_cert_payload = PEMCertificatePayload(config.prefix + '.mdm-ca', str(mdm_ca.get_cacert().to_pem()).strip(), PayloadDisplayName='MDM CA Certificate')

    profile.append_payload(ca_cert_payload)

    for new_webcrt_profile in get_webcrts(config):
        profile.append_payload(new_webcrt_profile)

    push_cert = config.push_cert.to_x509(cert_type=PushCertificate)
    topic = push_cert.get_topic()

    # NOTE: any device requesting non-SCEP enrollment will be generating new
    # CA-signed certificates. may want to gate the enrollment page by password
    # or other authentication
    if config.device_identity_method == 'provide':
        # make new device privkey, certificate then CA sign and persist
        # certificate finally return new Identity object

        new_dev_ident, _ = mdm_ca.gen_new_device_identity()

        # random password for PKCS12 payload
        p12pw = os.urandom(20).encode('hex')

        # generate PCKS12 profile payload
        new_dev_ident_payload = PKCS12CertificatePayload(
            config.prefix + '.id-cert',
            new_dev_ident.to_pkcs12(p12pw),
            p12pw,
            PayloadDisplayName='Device Identity Certificate')

        profile.append_payload(new_dev_ident_payload)
        cert_uuid = new_dev_ident_payload.get_uuid()
    elif config.device_identity_method == 'ourscep':
        # SCEP is preferred
        scep_config = db_session.query(SCEPConfig).one()

        scep_payload = SCEPPayload(
            config.prefix + '.mdm-scep',
            config.scep_url,
            PayloadContent=dict(
                Keysize=2048,
                Challenge=scep_config.challenge,
                # CAFingerprint=plistlib.Data(mdm_ca.get_cacert().get_m2_cert().get_fingerprint('sha1').decode('hex')),
                # Subject=[
                #     [ ['CN', 'MDM Enrollment'] ],
                # ],
                ),
            PayloadDisplayName='MDM SCEP')
        profile.append_payload(scep_payload)
        cert_uuid = scep_payload.get_uuid()
    else:
        abort(500, 'Invalid device identity method')

    new_mdm_payload = MDMPayload(
        config.prefix + '.mdm',
        cert_uuid,
        topic, # APNs push topic
        config.mdm_url,
        config.access_rights,
        CheckInURL=config.checkin_url,
        # we can validate MDM device client certs provided via SSL/TLS.
        # however this requires an SSL framework that is able to do that.
        # alternatively we may optionally have the client digitally sign the
        # MDM messages in an HTTP header. this method is most portable across
        # web servers so we'll default to using that method. note it comes
        # with the disadvantage of adding something like 2KB to every MDM
        # request
        SignMessage=True,
        CheckOutWhenRemoved=True,
        ServerCapabilities=['com.apple.mdm.per-user-connections'], # per-network user & mobile account authentication (OS X extensions)
        PayloadDisplayName='Device Configuration and Management')

    profile.append_payload(new_mdm_payload)

    return profile.generate_plist()

def handle_authenticate(resp):
    """Handle authentication"""

    # TODO: check to make sure device == UDID == cert, etc.
    try:
        device = db_session.query(Device).filter(Device.udid == resp['UDID']).one()
        if device.certificate and g.device_cert != device.certificate:
            # TODO: test if current certificate is in use by another device
            # if not then assume it's probably okay to use, otherwise
            # throw an error?
            if TRUST_DEV_PROVIDED_CERT:
                # this is /probably/ okay because our @device_cert_check
                # decorator makes sure that the cert originated in our DB
                # however shenanegans could be going on where two devices
                # try to enroll using the same-cert profile, so best to block
                # here
                print 'WARNING: device provided identity cert does not' \
                    ' match issued cert! (possibly a re-enrollment?)'
                db_session.delete(device.certificate)
            else:
                raise Exception('device provided identity cert does not' \
                    ' match issued cert! (possibly a re-enrollment?)')
    except NoResultFound:
        # no device found, let's make a new one!
        device = Device()
        print "GOT ENROL POST"
        current_app.logger.info("GOT ENROL POST")
        db_session.add(device)

        # PTW: This would be ideal place to notify another service,
        # but only MDMs get the UDID, so any other service will have
        # to match the device by serial number - we don't have that
        # yet.
        device.udid = resp['UDID']
        enroll.notify_enrolled(device.udid)

    if 'Topic' in resp:
        device.topic = resp['Topic']

    # remove the previous device token (in the case of a re-enrollment) to
    # tell the difference between a periodic TokenUpdate and the first
    # post-enrollment TokenUpdate
    device.token = None
    device.first_user_message_seen = False

    # TODO: we're essentially trusting the device to give the correct security infomration here
    device.certificate = g.device_cert

    db_session.commit()
    #db_session.query(QueuedCommand).filter(QueuedCommand.device_id == device.id).delete()
    #db_session.delete(device)
    #db_session.commit()

    return 'OK'

def handle_token_update(resp, print_resp):
    """Handle a token update"""

    current_app.logger.info('TokenUpdate received')
    print print_resp

    # TODO: a TokenUpdate can either be for a device or a user (per OS X extensions)
    if 'UserID' in resp:
        current_app.logger.warn('per-user TokenUpdate not yet implemented, skipping')
        return 'OK'

    # TODO: check to make sure device == UDID == cert, etc.
    device = db_session.query(Device).filter(Device.udid == resp['UDID']).one()

    # device.certificate = g.device_cert

    if 'PushMagic' in resp:
        device.push_magic = resp['PushMagic']

    if 'Topic' in resp:
        device.topic = resp['Topic']

    first_token_update = False if device.token else True

    if 'Token' in resp:
        device.token = resp['Token'].data.encode('base64')
    else:
        current_app.logger.error('TokenUpdate message missing Token')
        abort(400, 'invalid data supplied')

    if 'UnlockToken' in resp:
        device.unlock_token = resp['UnlockToken'].data.encode('base64')

    db_session.commit()

    if first_token_update:
        # the first TokenUpdate implies successful MDM profile install.
        # kick off our first-device commands, noting any DEP Await state
        current_app.logger.info('sending initial post-enrollment MDM command(s) to device=%d', g.device.id)
        device_first_post_enroll(g.device, awaiting=resp.get('AwaitingConfiguration', False))

    return 'OK'

def handle_user_authenticate(resp, print_resp):
    """Handle a user authentication message"""

    print print_resp
    current_app.logger.warn('per-user authentication not yet implemented, skipping')
    abort(410, 'per-user authentication not yet supported')
    # TODO: we can theoretically do a digest authentication on the actual
    # end-user's password supplied at the login screen. this will depend
    # depend heavily on any given user's backend. Perhaps provide some
    # functionality of auth plugins against AD, OD, etc.
    if 'DigestResponse' not in resp:
        print 'no DigestResponse, generating'
        config = db_session.query(MDMConfig).one()

        # no digest necessary and thus no AuthToken necessary for this OS X user
        # digdict = {'DigestChallenge': ''}

        digdict = {'DigestChallenge': 'Digest nonce="%s",realm="%s"' % (os.urandom(20).encode('base64'), config.prefix)}

        print digdict

        resp = make_response(plistlib.writePlistToString(digdict))
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    else:
        print 'DigestResponse!'
        print print_resp

        tokdict = {'AuthToken': os.urandom(20).encode('hex')}
        print tokdict


        resp = make_response(plistlib.writePlistToString(tokdict))
        resp.headers['Content-Type'] = 'application/xml'
        return resp

        # respond with an AuthToken for the user, all future MDM commands will include this coming from the user

def do_checkin():
    """Check in from device"""
    resp = g.plist_data
    print_resp = resp.copy()

    if 'UnlockToken' in print_resp:
        # hide the unlocktoken since it's pretty large
        print_resp['UnlockToken'] = '[Hiding Unlock Token]'

    if resp['MessageType'] == 'Authenticate':
        return handle_authenticate(resp)
    elif resp['MessageType'] == 'TokenUpdate':
        return handle_token_update(resp, print_resp)
    elif resp['MessageType'] == 'UserAuthenticate':
        return handle_user_authenticate(resp, print_resp)
    else:
        print 'Unknown message type', resp['MessageType']
        print print_resp

    # a best-effort notification to the MDM system the MDM profile has been removed
    # only sent CheckOutWhenRemoved
    # elif resp['MessageType'] == 'CheckOut':

    print 'Invalid message type'
    abort(500, 'Invalid message type')

def check_device_status(plist):
    """Ensure device is ready given its MDM check"""

    if 'Status' not in plist:
        current_app.logger.error('invalid MDM request (no Status provided) from device id %d' % g.device.id)
        abort(400, 'invalid input data')
    else:
        status = plist['Status']

    current_app.logger.info('device id=%d udid=%s processing status=%s', g.device.id, g.device.udid, status)

    print plist

    if status != 'Idle':

        if 'CommandUUID' not in plist:
            current_app.logger.error('missing CommandUUID for non-Idle status')
            abort(400, 'invalid input data')

        try:
            command = QueuedCommand.find_by_uuid(plist['CommandUUID'])

            # update the status of this command and commit
            command.result = status
            command.set_responded()
            db_session.commit()

            # find the MDM class that this QueuedCommand was generated from
            cmd_class = find_mdm_command_class(command.command_class)

            if not cmd_class:
                command.set_invalid()
                db_session.commit()
                current_app.logger.info('no matching QueuedMDMCommand class for %s', command.command_class)
            else:
                # instantiate it
                mdm_command = cmd_class.from_queued_command(g.device, command)

                # the individual commands will need to be aware of and handle
                # any Acknowledged/Error/CommandFormatError/Idle/NotNow
                # differences. except for the NotNow status any and all
                # handling is up the specific command class
                mdm_command.process_response_dict(plist)

        except NoResultFound:
            current_app.logger.info('no record of command uuid=%s', plist['CommandUUID'])

    if status == 'NotNow':
        current_app.logger.warn('NotNow status received, forgoing any further commands')
        return False

    return True

def do_mdm():
    """Execute MDM actions"""
    if g.device.udid != g.plist_data['UDID']:
        # see note in device_cert_check() about old device cert sometimes
        # being provided
        current_app.logger.info('provided UDID does not match device UDID')
        abort(400, 'invalid input data')

    if 'UserID' in g.plist_data:
        # Note that with DEP this is an opportune time to queue up an
        # application install for the /device/ despite this being a per-user
        # MDM command. this is becasue DEP appears to only allow apps to be
        # installed while a user is logged in. note also the undocumented
        # NotOnConsole key to (possibly) indicate that this is a UI login?
        device_first_user_message(g.device)
        current_app.logger.warn('per-user MDM command not yet supported')
        return ''

    if not check_device_status(g.plist_data):
        return ''

    while True:
        command = QueuedCommand.get_next_device_command(g.device)

        if not command:
            break

        # mark this command as being in process right away to (try) to avoid
        # any race conditions with mutliple MDM commands from the same device
        # at a time
        command.set_processing()
        db_session.commit()

        # find the MDM class that this QueuedCommand was generated from
        cmd_class = find_mdm_command_class(command.command_class)

        if not cmd_class:
            command.set_invalid()
            db_session.commit()
            current_app.logger.info('no matching QueuedMDMCommand class for %s', command.command_class)
            continue

        # instantiate it
        mdm_command = cmd_class.from_queued_command(g.device, command)

        # get command dictionary representation (e.g. the full command to send)
        output_dict = mdm_command.generate_dict()

        current_app.logger.info('sending %s MDM command class=%s to device=%d', mdm_command.request_type, command.command_class, g.device.id)

        # convert to plist and send
        resp = make_response(plistlib.writePlistToString(output_dict))
        resp.headers['Content-Type'] = 'application/xml'

        # finally set as sent
        command.set_sent()
        db_session.commit()

        return resp

    current_app.logger.info('no further MDM commands for device=%d', g.device.id)
    # return empty response as we have no further work
    return ''

def do_send_dev_info(dev_id):
    """Get the info for a device"""
    device = db_session.query(Device).filter(Device.id == dev_id).one()

    new_qc = UpdateInventoryDevInfoCommand.new_queued_command(device)
    db_session.add(new_qc)

    db_session.commit()

    push_to_device(device)

    return 'OK'

def do_app_manifest(app_id):
    """Request a manifest for an app"""
    app_q = db_session.query(App).filter(App.id == app_id)
    app = app_q.one()

    config = db_session.query(MDMConfig).one()

    asset = {
        'kind': 'software-package',
        'md5-size': app.md5_chunk_size,
        'md5s': app.md5_chunk_hashes.split(':'),
        'url': '%s/app/%d/download/%s' % (config.base_url(), app_id, app.filename),
        }

    metadata = {'kind': 'software', 'title': app.filename, 'sizeInBytes': app.filesize}

    pkgs_ids = app.pkg_ids_json
    pkgs_bundles = [{'bundle-identifier': i[0], 'bundle-version': i[1]} for i in pkgs_ids]

    # if subtitle:
    #     metadata['subtitle'] = subtitle

    metadata.update(pkgs_bundles[0])

    if len(pkgs_bundles) > 1:
        metadata['items'] = pkgs_bundles

    download = {'assets': [asset, ], 'metadata': metadata}

    manifest = {'items': [download]}

    resp = make_response(plistlib.writePlistToString(manifest))
    resp.headers['Content-Type'] = 'application/xml'
    return resp

def do_app_download(app_id, filename):
    """Instruct a device to download an app"""
    app_q = db_session.query(App).filter(App.id == app_id)
    app = app_q.one()

    # FIXME: surely filename should be used here somewhere?
    current_app.logger.info('Request to download: ' + str(filename))

    return send_file(os.path.join(current_app.config['APP_UPLOAD_ROOT'], app.path_format()))

def do_mdm_payload():
    """Create a response containing an MDM configuration"""
    plist = generate_mdm_payload()

    resp = make_response(plist)
    resp.headers['Content-Type'] = PROFILE_CONTENT_TYPE
    return resp
