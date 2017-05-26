from uuid import uuid4

from cryptography.hazmat.backends import default_backend
from flask import current_app, render_template, abort, Blueprint, make_response, url_for
import os
from .profiles.models import MDMPayload, Profile, PEMCertificatePayload, SCEPPayload
from .profiles import PROFILE_CONTENT_TYPE, schema as profile_schema, PayloadScope
from .models import db, Organization, SCEPConfig
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .plistlib.nonewriter import dumps as dumps_none
from cryptography import x509
from cryptography.x509.oid import NameOID

enroll_app = Blueprint('enroll_app', __name__)


@enroll_app.route('/')
def index():
    """Show the enrollment page"""
    return render_template('enroll.html')


def base64_to_pem(crypto_type, b64_text, width=76):
    lines = ''
    for pos in range(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)


@enroll_app.route('/profile', methods=['GET', 'POST'])
def enroll():
    """Generate an enrollment profile."""
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    push_certificate_path = os.path.join(os.path.dirname(current_app.root_path), current_app.config['PUSH_CERTIFICATE'])

    try:
        scep_config = db.session.query(SCEPConfig).one()
    except NoResultFound:
        abort(500, 'No SCEP Configuration found, cannot generate enrollment profile.')

    if os.path.exists(push_certificate_path):
        push_certificate_basename, ext = os.path.splitext(push_certificate_path)
        if ext.lower() == '.p12':  # push service will have re-exported the PKCS#12 container
            push_certificate_path = push_certificate_basename + '.crt'

        with open(push_certificate_path, 'rb') as fd:
            push_certificate = x509.load_pem_x509_certificate(fd.read(), backend=default_backend())
    else:
        abort(500, 'No push certificate available at: {}'.format(push_certificate_path))

    if not org:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    if not org.payload_prefix:
        abort(500, 'MDM configuration has no profile prefix')

    # profile = Profile(org.payload_prefix + '.enroll', PayloadDisplayName=org.name)
    profile = Profile(
        identifier=org.payload_prefix + '.enroll',
        uuid=uuid4(),
        display_name='Commandment Enrollment Profile',
        description='Enrolls your device for Mobile Device Management',
        organization=org.name,
        version=1,
        scope=PayloadScope.System,
    )

    if 'CA_CERTIFICATE' in current_app.config:
        with open(current_app.config['CA_CERTIFICATE'], 'rb') as fd:
            pem_data = fd.read()
            pem_payload = PEMCertificatePayload(
                uuid=uuid4(),
                identifier=org.payload_prefix + '.ca',
                payload_content=pem_data,
                display_name='Certificate Authority',
            )
            profile.payloads.append(pem_payload)

    # Include Self Signed Certificate if necessary
    # TODO: Check that cert is self signed.
    if 'SSL_CERTIFICATE' in current_app.config:
        basepath = os.path.dirname(__file__)
        certpath = os.path.join(basepath, current_app.config['SSL_CERTIFICATE'])
        with open(certpath, 'rb') as fd:
            pem_data = fd.read()
            pem_payload = PEMCertificatePayload(
                uuid=uuid4(),
                identifier=org.payload_prefix + '.ssl',
                payload_content=pem_data,
                display_name='Web Server Certificate',
            )
            profile.payloads.append(pem_payload)

    scep_payload = SCEPPayload(
        uuid=uuid4(),
        identifier=org.payload_prefix + '.mdm-scep',
        url=scep_config.url,
        name='MDM SCEP',
        subject=[['CN', '%HardwareUUID%']],
        challenge=scep_config.challenge,
        key_size=2048,
        key_type='RSA',
        display_name='MDM SCEP',
    )

    profile.payloads.append(scep_payload)
    cert_uuid = scep_payload.uuid

    from .mdm import AccessRights

    push_topics = push_certificate.subject.get_attributes_for_oid(NameOID.USER_ID)
    if len(push_topics) != 1:
        abort(500, 'Unexpected missing or invalid push topic in Push Certificate')

    push_topic = push_topics[0].value

    mdm_payload = MDMPayload(
        uuid=uuid4(),
        identifier=org.payload_prefix + '.mdm',
        identity_certificate_uuid=cert_uuid,
        topic=push_topic,
        server_url='https://{}:{}/mdm'.format(current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']),
        access_rights=AccessRights.All.value,
        check_in_url='https://{}:{}/checkin'.format(current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']),
        sign_message=True,
        check_out_when_removed=True,
        display_name='Device Configuration and Management',
        server_capabilities=['com.apple.mdm.per-user-connections'],
    )
    profile.payloads.append(mdm_payload)

    schema = profile_schema.ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


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