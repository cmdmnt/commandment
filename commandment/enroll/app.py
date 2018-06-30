"""
The enroll blueprint covers all enrolment scenarios such as:

- Over-the-Air profile delivery
- Direct enrolment (delivering a com.apple.mdm payload)

"""

from uuid import uuid4
import plistlib

from flask import current_app, render_template, abort, Blueprint, make_response, url_for, request, g
import os

from commandment.enroll import AllDeviceAttributes
from commandment.enroll.profiles import ca_trust_payload_from_configuration, scep_payload_from_configuration, \
    identity_payload
from commandment.profiles.models import MDMPayload, Profile, PEMCertificatePayload, DERCertificatePayload, SCEPPayload
from commandment.profiles import PROFILE_CONTENT_TYPE, plist_schema as profile_schema, PayloadScope
from commandment.models import db, Organization, SCEPConfig
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from commandment.plistutil.nonewriter import dumps as dumps_none
from commandment.enroll.util import generate_enroll_profile
from commandment.cms.decorators import verify_cms_signers
from commandment.pki.ca import get_ca

enroll_app = Blueprint('enroll_app', __name__)


def base64_to_pem(crypto_type, b64_text, width=76):
    lines = ''
    for pos in range(0, len(b64_text), width):
        lines += b64_text[pos:pos + width] + '\n'

    return '-----BEGIN %s-----\n%s-----END %s-----' % (crypto_type, lines, crypto_type)


@enroll_app.route('/trust.mobileconfig', methods=['GET'])
def trust_mobileconfig():
    """Generate a trust profile, if one is required.

    :resheader Content-Type: application/x-apple-aspen-config
    :statuscode 200:
    :statuscode 500: The system has not been configured, so we can't produce anything.
    """
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
        # If you specified a CA certificate, we assume it isn't a CA trusted by Apple devices.
        ca_payload = ca_trust_payload_from_configuration()
        profile.payloads.append(ca_payload)

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

    ca = get_ca()
    key, csr = ca.create_device_csr('device-identity')
    device_certificate = ca.sign(csr)

    pkcs12_payload = identity_payload(key, device_certificate, 'sekret')
    profile = generate_enroll_profile(pkcs12_payload)

    schema = profile_schema.ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


@enroll_app.route('/ota')
def ota_enroll():
    """Over-The-Air Profile Delivery Phase 1.5.

    This endpoint represents the delivery of the `Profile Service` profile that should be delivered AFTER the user has
    successfully authenticated.
    """
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
            'URL': 'https://{}:{}/enroll/ota_authenticate'.format(
                current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']
            ),
            'DeviceAttributes': list(AllDeviceAttributes),
            'Challenge': 'TODO',
        }],
    }
    plist_data = dumps_none(profile)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


@enroll_app.route('/ota_authenticate', methods=['POST'])
@verify_cms_signers
def ota_authenticate():
    """Over-The-Air Profile Delivery Phase 3 and 4.

    This endpoint represents the OTA Phase 3 and 4, "/profile" endpoint as specified in apples document "Over-The-Air
    Profile Delivery".

    There are two types of requests made here:
    - The first request is signed by the iPhone Device CA and contains the challenge in the `Profile Service` payload,
        we respond with the SCEP detail.
    - The second request is signed by the issued SCEP certificate. We should respond with an enrollment profile.
        It also contains the same device attributes sent in the previous step, but this time they are authenticated by
        our SCEP CA.

    Examples:

    Signed plist given in the first request::

        {
            'CHALLENGE': '<CHALLENGE FROM PROFILE HERE>',
            'IMEI': 'empty if macOS',
            'MEID': 'empty if macOS',
            'NotOnConsole': False,
            'PRODUCT': 'MacPro6,1',
            'SERIAL': 'C020000000000',
            'UDID': '00000000-0000-0000-0000-000000000000',
            'UserID': '00000000-0000-0000-0000-000000000000',
            'UserLongName': 'Joe User',
            'UserShortName': 'juser',
            'VERSION': '16F73'
        }

    See Also:
        - `Over-the-Air Profile Delivery and Configuration <https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/iPhoneOTAConfiguration/Introduction/Introduction.html#//apple_ref/doc/uid/TP40009505-CH1-SW1>`_.
    """
    signed_data = g.signed_data
    signers = g.signers
    # TODO: This should Validate to iPhone Device CA but we can't because:
    # http://www.openradar.me/31423312
    device_attributes = plistlib.loads(signed_data)

    current_app.logger.debug(device_attributes)

    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    # TODO: Behold, the stupidest thing ever just to get this working, theres no way this should be prod:
    # Phase 4 does not send a challenge but phase 3 does
    if 'CHALLENGE' in device_attributes:
        # Reply SCEP
        profile = Profile(
            identifier=org.payload_prefix + '.ota.phase3',
            uuid=uuid4(),
            display_name='Commandment OTA SCEP Enrollment',
            description='Retrieves a SCEP Certificate to complete OTA Enrollment',
            organization=org.name,
            version=1,
            scope=PayloadScope.System,
        )

        scep_payload = scep_payload_from_configuration()
        profile.payloads.append(scep_payload)
    else:
        profile = generate_enroll_profile()
    # profile = generate_enroll_profile()

    schema = profile_schema.ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}

