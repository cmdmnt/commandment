import sqlalchemy.orm.exc
import datetime
import dateutil.parser

from flask import Blueprint, jsonify, g, current_app, abort, request
from flask_rest_jsonapi import Api
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509 import NameOID
from base64 import urlsafe_b64encode

from commandment.models import db
from commandment.pki.models import RSAPrivateKey, CertificateSigningRequest
from commandment.dep.models import DEPServerTokenCertificate, DEPAccount
from commandment.enroll.util import generate_enroll_profile
from commandment.cms.decorators import verify_cms_signers
from commandment.plistutil.nonewriter import dumps as dumps_none
from commandment.profiles.plist_schema import ProfileSchema
from commandment.profiles import PROFILE_CONTENT_TYPE
from commandment.pki.ca import get_ca
from commandment.dep import smime

from .resources import DEPProfileList, DEPProfileDetail, DEPProfileRelationship, DEPAccountList, DEPAccountDetail
import plistlib
import json

dep_app = Blueprint('dep_app', __name__)
api = Api(blueprint=dep_app)

api.route(DEPProfileList, 'dep_profile_list', '/api/v1/dep/profiles/')
api.route(DEPProfileDetail, 'dep_profile_detail', '/api/v1/dep/profiles/<int:dep_profile_id>')
api.route(DEPProfileRelationship, 'dep_profile_devices',
          '/api/v1/dep/profiles/<int:dep_profile_id>/relationships/devices')
api.route(DEPAccountList, 'dep_account_list', '/api/v1/dep/accounts/')
api.route(DEPAccountDetail, 'dep_account_detail', '/api/v1/dep/accounts/<int:dep_account_id>')


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
        request_model.rsa_private_key = private_key_model
        db.session.add(request_model)

        certificate = ca.sign(request)
        certificate_model = DEPServerTokenCertificate.from_crypto(certificate)
        certificate_model.rsa_private_key = private_key_model
        db.session.add(certificate_model)

        db.session.commit()

    return certificate_model.pem_data, 200, {'Content-Type': 'application/x-x509-ca-cert',
                                             'Content-Disposition': 'attachment; filename="commandment-dep.cer"'}


@dep_app.route('/dep/stoken/upload', methods=["POST"])
def stoken_upload():
    """Upload the smime.p7m supplied from the DEP, ASM or ABM portals and decrypt it with a matching private key from
    our database, storing the result in the ``dep_configurations`` table.

    :reqheader Accept: application/vnd.api+json
    :reqheader Content-Type: multipart/form-data
    :statuscode 200: token decrypted ok
    :statuscode 400: token was unable to be decrypted.
    :statuscode 500: system error
    """
    if 'file' not in request.files:
        abort(400, 'no file uploaded in request data')

    f = request.files['file']

    try:
        certificate_model = db.session.query(DEPServerTokenCertificate).filter_by(x509_cn='COMMANDMENT-DEP').one()
    except sqlalchemy.orm.exc.NoResultFound:
        return abort(400, "No DEP certificate generated, impossible to decrypt the DEP token")

    pk: RSAPrivateKey = certificate_model.rsa_private_key
    if pk is None:
        return abort(500, 'Missing RSA Private Key for uploaded DEP token.')
    pk_crypto = pk.to_crypto()

    smime_data = f.read()
    payload = smime.decrypt(smime_data, pk_crypto)

    # dirty, dirty hacks for now. python email does not strip boundaries
    payload = payload.replace('-----BEGIN MESSAGE-----', '').replace('-----END MESSAGE-----', '')

    try:
        stoken = json.loads(payload)
    except json.decoder.JSONDecodeError:
        current_app.logger.debug(payload)
        return abort(400, "Failed to decode token, could not parse JSON data inside S/MIME data")

    try:
        dep_account = db.session.query(DEPAccount).one()
    except sqlalchemy.orm.exc.NoResultFound:
        dep_account = DEPAccount()

    dep_account.certificate = certificate_model
    dep_account.consumer_key = stoken['consumer_key']
    dep_account.consumer_secret = stoken['consumer_secret']
    dep_account.access_token = stoken['access_token']
    dep_account.access_secret = stoken['access_secret']
    dep_account.access_token_expiry = dateutil.parser.parse(stoken['access_token_expiry'])
    dep_account.token_updated_at = datetime.datetime.utcnow()

    db.session.commit()
    current_app.logger.debug('Saved DEP stoken')

    return jsonify(stoken)


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
