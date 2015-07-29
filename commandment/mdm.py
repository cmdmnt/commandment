'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, render_template, make_response, request, abort
from .pki.ca import get_ca, PushCertificate
from .pki.m2certs import Certificate, RSAPrivateKey
from .database import db_session, NoResultFound
from .models import MDMConfig, Certificate as DBCertificate, Device, PrivateKey as DBPrivateKey, QueuedCommand
from .profiles import Profile
from .profiles.cert import PEMCertificatePayload, PKCS12CertificatePayload
from .profiles.mdm import MDMPayload
from .mdmcmds import UpdateInventoryDevInfoCommand, find_mdm_command_class
from os import urandom
from M2Crypto import SMIME, BIO, X509
import plistlib
from .push import send_mdm_apns_notifications

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'

mdm_app = Blueprint('mdm_app', __name__)

@mdm_app.route('/')
def index():
    return render_template('enroll.html')

@mdm_app.route('/webcerts')
def webcerts():
    config = db_session.query(MDMConfig).one()

    profile = Profile(config.prefix + '.webcrt', PayloadDisplayName='MDM Web Cert Profile')

    # find and include all mdm.webcrt's
    q = db_session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.webcrt')
    for i, cert in enumerate(q):
        new_webcrt_profile = PEMCertificatePayload(config.prefix + '.webcrt.%d' % i, str(cert.pem_certificate), PayloadDisplayName='Web Server Certificate')
        profile.append_payload(new_webcrt_profile)

    resp = make_response(profile.generate_plist())
    resp.headers['Content-Type'] = PROFILE_CONTENT_TYPE
    return resp

@mdm_app.route('/enroll')
def enroll():
    mdm_ca = get_ca()

    config = db_session.query(MDMConfig).first()

    if not config:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    profile = Profile(config.prefix, PayloadDisplayName=config.mdm_name)

    ca_cert_payload = PEMCertificatePayload(config.prefix + '.mdm-ca', mdm_ca.get_cacert().get_pem(), PayloadDisplayName='MDM CA Certificate')

    profile.append_payload(ca_cert_payload)

    # find and include all mdm.webcrt's
    q = db_session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.webcrt')
    for i, cert in enumerate(q):
        new_webcrt_profile = PEMCertificatePayload(config.prefix + '.webcrt.%d' % i, str(cert.pem_certificate), PayloadDisplayName='Web Server Certificate')
        profile.append_payload(new_webcrt_profile)

    db_push_cert = config.push_cert

    push_cert = PushCertificate.load(str(db_push_cert.pem_certificate))

    topic = push_cert.get_topic()

    # make new device privkey, certificate then CA sign and persist certificate finally return new Identity object

    # NOTE: any device requesting enrollment will be generating new CA-signed
    # certificates. may want to gate the enrollment page by password or other
    # authentication

    # NOTE2: at a high-level there are two choices for how to get client
    # identity certificates onto the device: 1. embeddeding an PKCS12
    # identitiy (what we're doing) and 2. using SCEP to hand off certificates.
    # Apple recommends the latter method but not everyone will have a SCEP
    # infrastructure and due to complexities we're using this methodology at
    # the moment
    new_dev_ident = mdm_ca.gen_new_device_identity()

    # random password for PKCS12 payload
    p12pw = urandom(20).encode('hex')

    # generate PCKS12 profile payload
    new_dev_ident_payload = PKCS12CertificatePayload(config.prefix + '.id-cert', new_dev_ident.gen_pkcs12(p12pw), p12pw, PayloadDisplayName='Device Identity Certificate')

    profile.append_payload(new_dev_ident_payload)

    new_mdm_payload = MDMPayload(
        config.prefix + '.mdm',
        new_dev_ident_payload.get_uuid(),
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

    resp = make_response(profile.generate_plist())
    resp.headers['Content-Type'] = PROFILE_CONTENT_TYPE
    return resp

def base64_to_pem(crypto_type, b64_text, width=76):
    lines = ''
    for pos in xrange(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)

def verify_mdm_signature(mdm_sig, req_data):
    '''Verify the client's supplied MDM signature and return the client certificate included in the signature.'''
    pkcs7_pem_sig = base64_to_pem('PKCS7', mdm_sig)

    p7_bio = BIO.MemoryBuffer(str(pkcs7_pem_sig))
    p7 = SMIME.load_pkcs7_bio(p7_bio)

    p7_signers = p7.get0_signers(X509.X509_Stack())

    mdm_ca = get_ca()

    # can probably directly use m2 certificate here
    ca_x509_bio = BIO.MemoryBuffer(mdm_ca.get_cacert().get_pem())
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
    signer.verify(p7, data_bio)

    return p7_signers[0].as_pem()

@mdm_app.route('/send_mdm/<int:dev_id>')
def send_mdm(dev_id):
    # find device
    q = db_session.query(Device).filter(Device.id == dev_id)

    device_push_details = []
    ctr = 0
    for device in q:
        device_push_details.append((device.token.decode('base64'), device.push_magic))
        ctr += 1

    if not device_push_details:
        return 'No devices!'

    # find APNS certificate
    # better would be to compare our topic subject to the certificate UID
    # object to see if they're a match, this would allow multiple APNS certs
    # as well.
    q = db_session.query(DBCertificate, DBPrivateKey).join(DBCertificate, DBPrivateKey.certificates).filter(DBCertificate.cert_type == 'mdm.pushcert')
    db_cert, db_pk = q.one()

    # this is probably not necessary, we could just pass the raw PEM files on
    # over to the OpenSSL context
    cert = Certificate.load(str(db_cert.pem_certificate))
    pk = RSAPrivateKey.load(str(db_pk.pem_key))

    send_mdm_apns_notifications(pk, cert, device_push_details)

    return 'Sent %d Push Notifications' % ctr

@mdm_app.route("/checkin", methods=['PUT'])
def checkin():
    dev_cert_pem = verify_mdm_signature(request.headers['Mdm-Signature'], request.data)

    # as e.g. passed in from a webserver (nginx in this example)
    # dev_cert_pem = request.headers['X-Ssl-Client-Cert'].replace('\n ', '\n')

    try:
        # reload cert as passed in as both a sanity check and to reformat
        # incase the PEM as passed in (from the web server) is different that
        # how OpenSSL/M2Crypto would have formatted it
        reloaded_cert = Certificate.load(str(dev_cert_pem))
        db_dev_cert = db_session.query(DBCertificate).filter(DBCertificate.pem_certificate == str(reloaded_cert.get_pem())).one()
    except NoResultFound:
        print 'Device certificate not found!'
        print reloaded_cert.get_pem()
        abort(400, 'Device certificate not found')

    resp = plistlib.readPlistFromString(request.data)
    print_resp = resp.copy()

    if 'UnlockToken' in print_resp:
        # hide the unlocktoken since it's pretty large
        print_resp['UnlockToken'] = '[Hiding Unlock Token]'

    if resp['MessageType'] == 'Authenticate':
        # TODO: check to make sure device == UDID == cert, etc.
        try:
            device = db_session.query(Device).filter(Device.udid == resp['UDID']).one()
            if not db_dev_cert == device.certificate:
                raise Exception('device provided identity cert does not match issued cert!')
        except NoResultFound:
            # no device found, let's make a new one!
            device = Device()

            device.udid = resp['UDID']

        if 'Topic' in resp:
            device.topic = resp['Topic']

        # TODO: we're essentially trusting the device to give the correct security infomration here
        device.certificate = db_dev_cert

        db_session.add(device)
        db_session.commit()

        return 'OK'
    elif resp['MessageType'] == 'TokenUpdate':
        # TODO: a TokenUpdate can either be for a device or a user (per OS X extensions)
        if 'UserID' in resp:
            print 'Skipping User Token Update'
            return 'OK'

        # TODO: check to make sure device == UDID == cert, etc.
        device = db_session.query(Device).filter(Device.udid == resp['UDID']).one()

        print 'TokenUpdate'
        print print_resp

        # device.certificate = db_dev_cert

        if 'PushMagic' in resp:
            device.push_magic = resp['PushMagic']

        if 'Topic' in resp:
            device.topic = resp['Topic']

        if 'Token' in resp:
            device.token = resp['Token'].data.encode('base64')

        if 'UnlockToken' in resp:
            device.unlock_token = resp['UnlockToken'].data.encode('base64')

        db_session.commit()

        # TokenUpdate implies successful MDM profile installation. let's kick off a check-in

        # queue next command in DB for device
        new_qc = UpdateInventoryDevInfoCommand.new_queued_command(device)
        db_session.add(new_qc)

        db_session.commit()

        send_mdm(device.id)

        return 'OK'
    elif resp['MessageType'] == 'UserAuthenticate':
        print print_resp
        # abort(410, 'OS X per-user authentication not yet supported')
        # TODO: we can theoretically do a digest authentication on the actual
        # end-user's password supplied at the login screen. this will depend
        # depend heavily on any given user's backend. Perhaps provide some
        # functionality of auth plugins against AD, OD, etc.
        if 'DigestResponse' not in resp:
            print 'no DigestResponse, generating'
            config = db_session.query(MDMConfig).one()

            # no digest necessary and thus no AuthToken necessary for this OS X user
            # digdict = {'DigestChallenge': ''}

            digdict = {'DigestChallenge': 'Digest nonce="%s",realm="%s"' % (urandom(20).encode('base64'), config.prefix)}

            print digdict

            resp = make_response(plistlib.writePlistToString(digdict))
            resp.headers['Content-Type'] = 'application/xml'
            return resp
        else:
            print 'DigestResponse!'
            print print_resp

            tokdict = {'AuthToken': urandom(20).encode('hex')}
            print tokdict


            resp = make_response(plistlib.writePlistToString(tokdict))
            resp.headers['Content-Type'] = 'application/xml'
            return resp

            # respond with an AuthToken for the user, all future MDM commands will include this coming from the user
    else:
        print 'Unknown message type', resp['MessageType']
        print print_resp

    # a best-effort notification to the MDM system the MDM profile has been removed
    # only sent CheckOutWhenRemoved
    # elif resp['MessageType'] == 'CheckOut':

    print 'Invalid message type'
    abort(500, 'Invalid message type')

@mdm_app.route("/mdm", methods=['PUT'])
def mdm():
    dev_cert = verify_mdm_signature(request.headers['Mdm-Signature'], request.data)

    # as passed in from webserver (nginx in our case)
    # dev_cert = request.headers['X-Ssl-Client-Cert'].replace('\n ', '\n')

    try:
        # reload cert as passed in as both a sanity check and to reformat
        # incase the PEM as passed in (from the web server) is different that
        # how OpenSSL/M2Crypto would have formatted it
        reloaded_cert = Certificate.load(str(dev_cert))
        db_dev_cert = db_session.query(DBCertificate).filter(DBCertificate.pem_certificate == str(reloaded_cert.get_pem())).one()
    except NoResultFound:
        print 'Certificate not found!'
        print dev_cert
        abort(400, 'Certificate not found')

    # From iPhone:
    #   Content-Type: application/x-apple-aspen-mdm
    # print request.headers
    try:
        result = plistlib.readPlistFromString(request.data)
    except:
        print 'Could not read plist from response!'
        abort(400, 'Could not parse returned plist!')

    try:
        device = db_session.query(Device).filter(Device.udid == result['UDID']).one()
    except NoResultFound:
        print 'Device not found'
        print result['UDID']
        abort(400, 'Device not found')

    if device.certificate != db_dev_cert:
        print device.certificate.id
        print db_dev_cert.id
        # NOTE: odd bug with a profile removal/re-add where it tries to auth with the old cert?!
        print 'Certificate does not match device!'
        abort(400, 'Certificate does not match device!')


    if 'Status' not in result:
        print 'Invalid MDM request (missing Status)'
        abort(400, 'Invalid MDM request (missing Status)')

    if result['Status'] != 'Idle':
        print 'Processing Status:', result['Status']

        if 'CommandUUID' not in result:
            print 'Invalid MDM request (missing CommandUUID)'
            abort(400, 'Invalid MDM request (missing CommandUUID)')

        try:
            command = QueuedCommand.find_by_uuid(result['CommandUUID'])

            # find the MDM class that this QueuedCommand was generated from
            cmd_class = find_mdm_command_class(command.command_class)

            if not cmd_class:
                command.set_invalid()
                db_session.commit()
                print 'No matching QueuedMDMCommand: %s' % command.command_class

            # instantiate it
            mdm_command = cmd_class.from_queued_command(device, command)

            mdm_command.process_response_dict(result)

        except NoResultFound:
            print 'No '


    # Status = Acknowledged, Error, CommandFormatError, Idle, NotNow

    # TODO: test for NotNow case as docs say if we get this it's unlikely
    # we'll be able to send more NowNow-able commands

    # find an outstanding queued command for this device
    command = QueuedCommand.get_next_device_command(device)

    if command:
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
            print 'No matching QueuedMDMCommand: %s' % command.command_class
            return ''

        # instantiate it
        mdm_command = cmd_class.from_queued_command(device, command)

        # get command dictionary representation
        output_dict = mdm_command.generate_dict()

        # convert to plist and send
        resp = make_response(plistlib.writePlistToString(output_dict))
        resp.headers['Content-Type'] = 'application/xml'

        # finally set as sent
        command.set_sent()
        db_session.commit()

        return resp

    print 'No further queued commands for this device'
    return ''
