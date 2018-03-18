from cryptography.hazmat.backends import default_backend
from flask import Blueprint, jsonify, g, current_app
from flask_rest_jsonapi import Api
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from base64 import urlsafe_b64encode
from commandment.enroll.util import generate_enroll_profile
from commandment.cms.decorators import verify_cms_signers
from commandment.plistutil.nonewriter import dumps as dumps_none
from commandment.profiles.plist_schema import ProfileSchema
from commandment.profiles import PROFILE_CONTENT_TYPE
from .resources import DEPProfileList, DEPProfileDetail, DEPProfileRelationship
import plistlib

dep_app = Blueprint('dep_app', __name__)
api = Api(blueprint=dep_app)

api.route(DEPProfileList, 'dep_profile_list', '/v1/dep/profiles/')
api.route(DEPProfileDetail, 'dep_profile_detail', '/v1/dep/profiles/<int:dep_profile_id>')
api.route(DEPProfileRelationship, 'dep_profile_devices', '/v1/dep/profiles/<int:dep_profile_id>/relationships/devices')


@dep_app.route('/v1/dep/account', methods=["GET"])
def account():
    pass


@dep_app.route('/dep/enroll', methods=["POST"])
@verify_cms_signers
def profile():
    """Accept a CMS Signed DER encoded XML data containing device information.

    This starts the DEP enrollment process. The absolute url to this endpoint should be present in the DEP profile's
    enrollment URL.

    The signed data contains a plist with the following keys:

    :UDID: The device’s UDID.
    :SERIAL: The device's Serial Number.
    :PRODUCT: The device’s product type: e.g., iPhone5,1.
    :VERSION: The OS version installed on the device: e.g., 7A182.
    :IMEI: The device’s IMEI (if available).
    :MEID: The device’s MEID (if available).
    :LANGUAGE: The user’s currently-selected language: e.g., en.

    See Also:
        - `Mobile Device Management Protocol: Request to a Profile URL <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW242>`_.
    """
    g.plist_data = plistlib.loads(g.signed_data)
    profile = generate_enroll_profile()

    schema = ProfileSchema()
    result = schema.dump(profile)
    plist_data = dumps_none(result.data, skipkeys=True)

    return plist_data, 200, {'Content-Type': PROFILE_CONTENT_TYPE}


@dep_app.route('/dep/anchor_certs', methods=["GET"])
def anchor_certs():
    """Download a list of certificates to trust the MDM

    The response is a JSON array of base64 encoded DER certs as described in the DEP profile creation documentation."""
    anchors = []

    if 'CA_CERTIFICATE' in current_app.config:
        with open(current_app.config['CA_CERTIFICATE'], 'rb') as fd:
            pem_data = fd.read()
            c: x509.Certificate = x509.load_pem_x509_certificate(pem_data, backend=default_backend())
            der = c.public_bytes(Encoding.DER)
            anchors.append(urlsafe_b64encode(der))

    if 'SSL_CERTIFICATE' in current_app.config:
        with open(current_app.config['SSL_CERTIFICATE'], 'rb') as fd:
            pem_data = fd.read()
            c: x509.Certificate = x509.load_pem_x509_certificate(pem_data, backend=default_backend())
            der = c.public_bytes(Encoding.DER)
            anchors.append(urlsafe_b64encode(der))

    return jsonify(anchors)
