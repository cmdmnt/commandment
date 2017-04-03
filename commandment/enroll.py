from flask import current_app, render_template, abort, Blueprint, make_response
import os
import codecs
from .pki.ca import get_ca
from .pki.models import Certificate
from .profiles.cert import PEMCertificatePayload, SCEPPayload
from .profiles.mdm import MDMPayload
from .profiles import Profile
from .models import db, Organization

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'

enroll_app = Blueprint('enroll_app', __name__)


@enroll_app.route('/enroll/')
def index():
    """Show the enrollment page"""
    return render_template('enroll.html')


def base64_to_pem(crypto_type, b64_text, width=76):
    lines = ''
    for pos in range(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)


@enroll_app.route('/enroll/profile', methods=['GET', 'POST'])
def enroll():
    """Generate an enrollment profile."""
    mdm_ca = get_ca()

    org = db.query(Organization).first()
    push_path = os.path.join(os.path.dirname(current_app.root_path), current_app.config['PUSH_CERTIFICATE'])

    if os.path.exists(push_path):
        with open(push_path, 'rb') as fd:
            push_cert = Certificate('mdm.pushcert')
            push_cert.pem_data = fd.read()
    else:
        abort(500, 'No push certificate available at: {}'.format(push_path))

    if not org:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    if not org.payload_prefix:
        abort(500, 'MDM configuration has no profile prefix')

    profile = Profile(org.payload_prefix + '.enroll', PayloadDisplayName=org.name)

    ca_cert_payload = PEMCertificatePayload(org.payload_prefix + '.mdm-ca', mdm_ca.certificate.pem_data,
                                            PayloadDisplayName='MDM CA Certificate')

    profile.append_payload(ca_cert_payload)

    # find and include all mdm.webcrt's
    # q = db_session.query(SSLCertificate).first()
    # for i, cert in enumerate(q):
    #     new_webcrt_profile = PEMCertificatePayload(org.payload_prefix + '.webcrt.%d' % i, str(cert.pem_data).strip(),
    #                                                PayloadDisplayName='Web Server Certificate')
    #     profile.append_payload(new_webcrt_profile)

    hexlify = codecs.getencoder('hex')
    ca_fingerprint = hexlify(mdm_ca.certificate.fingerprint)

    scep_payload = SCEPPayload(
        org.payload_prefix + '.mdm-scep',
        'http://localhost/scep',  # config.scep_url,
        PayloadContent=dict(
            Keysize=2048,
            Challenge='sekret',
            #CAFingerprint=plistlib.Data(ca_fingerprint),
            Subject=[
                [['CN', '%HardwareUUID%']]
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


# def device_first_post_enroll(device, awaiting=False):
#     print('enroll:', 'UpdateInventoryDevInfoCommand')
#     db.session.add(UpdateInventoryDevInfoCommand.new_queued_command(device))
#
#     # install all group profiles
#     for group in device.mdm_groups:
#         for profile in group.profiles:
#             db.session.add(InstallProfile.new_queued_command(device, {'id': profile.id}))
#
#     if awaiting:
#         # in DEP Await state, send DeviceConfigured to proceed with setup
#         db.session.add(DeviceConfigured.new_queued_command(device))
#
#     db.session.commit()
#
#     push_to_device(device)