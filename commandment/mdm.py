"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from flask import Blueprint, render_template, make_response, request, abort
from flask import current_app, send_file, g
from cryptography.hazmat.primitives import hashes
from .pki.models import Certificate
from .pki.ca import get_ca
from .database import db_session, NoResultFound, or_, and_
from .models import MDMConfig, Certificate as DBCertificate, Device, RSAPrivateKey as DBPrivateKey, QueuedCommand
from .models import App, MDMGroup, app_group_assoc, SCEPConfig, Organization, SSLCertificate
from .profiles import Profile
from .profiles.cert import PEMCertificatePayload, PKCS12CertificatePayload, SCEPPayload
from .profiles.mdm import MDMPayload
from .mdmcmds import UpdateInventoryDevInfoCommand, find_mdm_command_class
from .mdmcmds import InstallProfile, AppInstall
from .mdmcmds.dep import DeviceConfigured
from .decorators import device_cert_check, parse_plist_input_data
from os import urandom
import plistlib
from .push import push_to_device
import os

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'
TRUST_DEV_PROVIDED_CERT = True

mdm_app = Blueprint('mdm_app', __name__)


@mdm_app.route('/enroll/')
def index():
    """Show the enrollment page"""
    return render_template('enroll.html')


def base64_to_pem(crypto_type, b64_text, width=76):
    lines = ''
    for pos in range(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)


@mdm_app.route('/enroll/profile', methods=['GET', 'POST'])
def enroll():
    """Generate an enrollment profile."""
    mdm_ca = get_ca()

    org = db_session.query(Organization).first()

    if os.path.exists(current_app.config['PUSH_CERTIFICATE']):
        with open(current_app.config['PUSH_CERTIFICATE'], 'rb') as fd:
            push_cert = Certificate('mdm.pushcert')
            push_cert.pem_data = fd.read()
    else:
        abort(500, 'No push certificate available')

    if not org:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    if not org.payload_prefix:
        abort(500, 'MDM configuration has no profile prefix')

    profile = Profile(org.payload_prefix + '.enroll', PayloadDisplayName=org.name)

    ca_cert_payload = PEMCertificatePayload(org.payload_prefix + '.mdm-ca', str(mdm_ca.certificate.pem_data).strip(),
                                            PayloadDisplayName='MDM CA Certificate')

    profile.append_payload(ca_cert_payload)

    # find and include all mdm.webcrt's
    q = db_session.query(SSLCertificate).first()
    for i, cert in enumerate(q):
        new_webcrt_profile = PEMCertificatePayload(org.payload_prefix + '.webcrt.%d' % i, str(cert.pem_data).strip(),
                                                   PayloadDisplayName='Web Server Certificate')
        profile.append_payload(new_webcrt_profile)

    scep_payload = SCEPPayload(
        org.payload_prefix + '.mdm-scep',
        'http://localhost/scep',  # config.scep_url,
        PayloadContent=dict(
            Keysize=2048,
            Challenge='sekret',
            CAFingerprint=plistlib.Data(mdm_ca.certificate.fingerprint(hashes.SHA1()).decode('hex')),
            Subject=[
                [ ['CN', '%HardwareUUID%'] ]
            ]
        ),
        PayloadDisplayName='MDM SCEP')
    profile.append_payload(scep_payload)
    cert_uuid = scep_payload.get_uuid()
    # else:
    #     abort(500, 'Invalid device identity method')

    from .profiles.mdm import MDM_AR__ALL

    new_mdm_payload = MDMPayload(
        org.payload_prefix + '.mdm',
        cert_uuid,
        push_cert.topic,  # APNs push topic
        'https://localhost:5443/mdm',
        MDM_AR__ALL,
        CheckInURL='https://localhost:5443/checkin',
        # we can validate MDM device client certs provided via SSL/TLS.
        # however this requires an SSL framework that is able to do that.
        # alternatively we may optionally have the client digitally sign the
        # MDM messages in an HTTP header. this method is most portable across
        # web servers so we'll default to using that method. note it comes
        # with the disadvantage of adding something like 2KB to every MDM
        # request
        SignMessage=True,
        CheckOutWhenRemoved=True,
        ServerCapabilities=['com.apple.mdm.per-user-connections'],
        # per-network user & mobile account authentication (OS X extensions)
        PayloadDisplayName='Device Configuration and Management')

    profile.append_payload(new_mdm_payload)

    resp = make_response(profile.generate_plist())
    resp.headers['Content-Type'] = PROFILE_CONTENT_TYPE
    return resp


def device_first_post_enroll(device, awaiting=False):
    print('enroll:', 'UpdateInventoryDevInfoCommand')
    db_session.add(UpdateInventoryDevInfoCommand.new_queued_command(device))

    # install all group profiles
    for group in device.mdm_groups:
        for profile in group.profiles:
            db_session.add(InstallProfile.new_queued_command(device, {'id': profile.id}))

    if awaiting:
        # in DEP Await state, send DeviceConfigured to proceed with setup
        db_session.add(DeviceConfigured.new_queued_command(device))

    db_session.commit()

    push_to_device(device)


@mdm_app.route("/checkin", methods=['PUT'])
@device_cert_check(no_device_okay=True)
@parse_plist_input_data
def checkin():
    """MDM checkin endpoint."""
    resp = g.plist_data
    print_resp = resp.copy()

    if 'UnlockToken' in print_resp:
        # hide the unlocktoken since it's pretty large
        print_resp['UnlockToken'] = '[Hiding Unlock Token]'

    if resp['MessageType'] == 'Authenticate':
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
                    print('WARNING: device provided identity cert does not' \
                          ' match issued cert! (possibly a re-enrollment?)')
                    db_session.delete(device.certificate)
                else:
                    raise Exception('device provided identity cert does not' \
                                    ' match issued cert! (possibly a re-enrollment?)')
        except NoResultFound:
            # no device found, let's make a new one!
            device = Device()
            db_session.add(device)

            device.udid = resp['UDID']

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

        return 'OK'
    elif resp['MessageType'] == 'TokenUpdate':
        current_app.logger.info('TokenUpdate received')
        print(print_resp)

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
    elif resp['MessageType'] == 'UserAuthenticate':
        print(print_resp)
        current_app.logger.warn('per-user authentication not yet implemented, skipping')
        abort(410, 'per-user authentication not yet supported')
        # TODO: we can theoretically do a digest authentication on the actual
        # end-user's password supplied at the login screen. this will depend
        # depend heavily on any given user's backend. Perhaps provide some
        # functionality of auth plugins against AD, OD, etc.
        if 'DigestResponse' not in resp:
            print('no DigestResponse, generating')
            config = db_session.query(MDMConfig).one()

            # no digest necessary and thus no AuthToken necessary for this OS X user
            # digdict = {'DigestChallenge': ''}

            digdict = {
                'DigestChallenge': 'Digest nonce="%s",realm="%s"' % (urandom(20).encode('base64'), config.prefix)}

            print(digdict)

            resp = make_response(plistlib.writePlistToString(digdict))
            resp.headers['Content-Type'] = 'application/xml'
            return resp
        else:
            print('DigestResponse!')
            print(print_resp)

            tokdict = {'AuthToken': urandom(20).encode('hex')}
            print(tokdict)

            resp = make_response(plistlib.writePlistToString(tokdict))
            resp.headers['Content-Type'] = 'application/xml'
            return resp

            # respond with an AuthToken for the user, all future MDM commands will include this coming from the user
    else:
        print('Unknown message type', resp['MessageType'])
        print(print_resp)

    # a best-effort notification to the MDM system the MDM profile has been removed
    # only sent CheckOutWhenRemoved
    # elif resp['MessageType'] == 'CheckOut':

    print('Invalid message type')
    abort(500, 'Invalid message type')


def device_first_user_message(device):
    '''Queue the MDM commands appropriate for a first-user-message seen
    event. Currently used to inititate DEP app installations.'''

    device.first_user_message_seen = True

    for group in device.mdm_groups:
        app_q = db_session.query(App).join(app_group_assoc, and_(app_group_assoc.c.mdm_group_id == group.id,
                                                                 app_group_assoc.c.app_id == App.id)).filter(
            app_group_assoc.c.install_early == True)

        for app in app_q:
            db_session.add(AppInstall.new_queued_command(device, {'id': app.id}))

    db_session.commit()

    push_to_device(device)


@mdm_app.route("/mdm", methods=['PUT'])
@device_cert_check()
@parse_plist_input_data
def mdm():
    """MDM connection endpoint."""
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

    if 'Status' not in g.plist_data:
        current_app.logger.error('invalid MDM request (no Status provided) from device id %d' % g.device.id)
        abort(400, 'invalid input data')
    else:
        status = g.plist_data['Status']

    current_app.logger.info('device id=%d udid=%s processing status=%s', g.device.id, g.device.udid, status)

    print(g.plist_data)

    if status != 'Idle':

        if 'CommandUUID' not in g.plist_data:
            current_app.logger.error('missing CommandUUID for non-Idle status')
            abort(400, 'invalid input data')

        try:
            command = QueuedCommand.find_by_uuid(g.plist_data['CommandUUID'])

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
                mdm_command.process_response_dict(g.plist_data)

        except NoResultFound:
            current_app.logger.info('no record of command uuid=%s', g.plist_data['CommandUUID'])

    if status == 'NotNow':
        current_app.logger.warn('NotNow status received, forgoing any further commands')
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

        current_app.logger.info('sending %s MDM command class=%s to device=%d', mdm_command.request_type,
                                command.command_class, g.device.id)

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


@mdm_app.route('/send_dev_info/<int:dev_id>')
def send_dev_info(dev_id: int):
    """Queue a ``DeviceInformation`` command for the specified commandment device ID."""
    device = db_session.query(Device).filter(Device.id == dev_id).one()

    new_qc = UpdateInventoryDevInfoCommand.new_queued_command(device)
    db_session.add(new_qc)

    db_session.commit()

    push_to_device(device)

    return 'OK'


@mdm_app.route("/app/<int:app_id>/manifest")
def app_manifest(app_id: int):
    """Retrieve an application manifest for the specified application ID."""
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


@mdm_app.route("/app/<int:app_id>/download/<filename>")
def app_download(app_id: int, filename: str):
    """Download a file corresponding to the specified application ID."""
    app_q = db_session.query(App).filter(App.id == app_id)
    app = app_q.one()

    return send_file(os.path.join(current_app.config['APP_UPLOAD_ROOT'], app.path_format()))
