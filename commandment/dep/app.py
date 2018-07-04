import sqlalchemy.orm.exc

from cryptography.hazmat.backends import default_backend
from flask import Blueprint, jsonify, g, current_app, abort
from flask_rest_jsonapi import Api
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509 import NameOID
from base64 import urlsafe_b64encode

from commandment.models import db, RSAPrivateKey, CertificateSigningRequest
from commandment.dep.models import DEPServerTokenCertificate
from commandment.enroll.util import generate_enroll_profile
from commandment.cms.decorators import verify_cms_signers
from commandment.plistutil.nonewriter import dumps as dumps_none
from commandment.profiles.plist_schema import ProfileSchema
from commandment.profiles import PROFILE_CONTENT_TYPE
from commandment.pki.ca import get_ca

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


@dep_app.route('/dep/certificate/download', methods=["GET"])
def certificate_download():
    """Create a new key/certificate to upload to the DEP/ASM/ABM portal.

    The private key generated for this certificate will be the key recipient of the DEP S/MIME payload.
    """

    try:
        certificate_model = db.session.query(DEPServerTokenCertificate).filter_by(x509_cn='COMMANDMENT-DEP').one()
    except sqlalchemy.orm.exc.NoResultFound:
        ca = get_ca()
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        private_key_model = RSAPrivateKey.from_crypto(private_key)
        db.session.add(private_key_model)

        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'COMMANDMENT-DEP'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
        ])

        builder = x509.CertificateSigningRequestBuilder()
        builder = builder.subject_name(name)
        builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)

        request = builder.sign(
            private_key,
            hashes.SHA256(),
            default_backend()
        )
        request_model = CertificateSigningRequest.from_crypto(request)
        db.session.add(request_model)

        certificate = ca.sign(request)
        certificate_model = DEPServerTokenCertificate.from_crypto(certificate)
        db.session.add(certificate_model)

        db.session.commit()

    return certificate_model.pem_data, 200, {'Content-Type': 'application/x-x509-ca-cert',
                                             'Content-Disposition': 'attachment; filename="commandment-dep.cer"'}


@dep_app.route('/dep/stoken/upload', methods=["POST"])
def stoken_upload():
    """Upload the smime.p7m supplied from the DEP, ASM or ABM portals and decrypt it with a matching private key from
    our database, storing the result in the ``dep_configurations`` table."""
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
