from uuid import uuid4
import plistlib

from flask import current_app, render_template, abort, Blueprint, make_response, url_for, request, g
import os

from commandment.enroll import AllDeviceAttributes
from commandment.profiles.models import MDMPayload, Profile, PEMCertificatePayload, DERCertificatePayload, SCEPPayload
from commandment.profiles import PROFILE_CONTENT_TYPE, plist_schema as profile_schema, PayloadScope
from commandment.models import db, Organization, SCEPConfig
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from commandment.plistutil.nonewriter import dumps as dumps_none
from commandment.enroll.util import generate_enroll_profile
from commandment.cms.decorators import verify_cms_signers

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


@enroll_app.route('/trust.mobileconfig', methods=['GET'])
def trust_mobileconfig():
    """Generate a trust profile, if one is required."""
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    profile = Profile(
        identifier=org.payload_prefix + '.trust',
        uuid=uuid4(),
        display_name='Commandment Trust Profile',
        description='Allows your device to trust the MDM server',
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
                description='Required for your device to trust the server',
                type='com.apple.security.root',
                version=1
            )
            profile.payloads.append(pem_payload)

    if 'SSL_CERTIFICATE' in current_app.config:
        basepath = os.path.dirname(__file__)
        certpath = os.path.join(basepath, current_app.config['SSL_CERTIFICATE'])
        with open(certpath, 'rb') as fd:
            pem_payload = PEMCertificatePayload(
                uuid=uuid4(),
                identifier=org.payload_prefix + '.ssl',
                payload_content=fd.read(),
                display_name='Web Server Certificate',
                description='Required for your device to trust the server',
                type='com.apple.security.pkcs1',
                version=1
            )
            profile.payloads.append(pem_payload)

    schema = profile_schema.ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE,
                             'Content-Disposition': 'attachment; filename="trust.mobileconfig"'}


@enroll_app.route('/profile', methods=['GET', 'POST'])
def enroll():
    """Generate an enrollment profile."""
    profile = generate_enroll_profile()

    schema = profile_schema.ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


@enroll_app.route('/ota')
def ota_enroll():
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    profile = {
        'PayloadType': 'Profile Service',
        'PayloadIdentifier': org.payload_prefix + '.ota.enroll',
        'PayloadUUID': str(uuid4()),
        'PayloadVersion': 1,
        'PayloadDisplayName': 'Commandment Profile Service',
        'PayloadDescription': 'Enrolls your device with Commandment',
        'PayloadContent': [{
            'URL': 'https://{}:{}/enroll/ota_authenticate'.format(current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']),
            'DeviceAttributes': list(AllDeviceAttributes),
            'Challenge': 'TODO',
        }],
    }
    plist_data = dumps_none(profile)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


@enroll_app.route('/ota_authenticate', methods=['POST'])
@verify_cms_signers
def ota_authenticate():
    signed_data = g.signed_data
    signers = g.signers
    device_attributes = plistlib.loads(signed_data)
    current_app.logger.debug(device_attributes)
