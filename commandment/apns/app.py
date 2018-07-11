from datetime import datetime
from flask import Blueprint, request, abort, send_file, current_app, jsonify
from sqlalchemy.orm.exc import NoResultFound

from base64 import b64encode
from commandment.models import db, Device, Certificate, RSAPrivateKey, CertificateSigningRequest, CACertificate, \
    EncryptionCertificate
from commandment.pki import serialization, ssl
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from .push import push_to_device
from .schema import PushResponseFlatSchema
from .mdmcert import submit_mdmcert_request
import ssl

api_push_app = Blueprint('api_push_app', __name__)

MDMCERT_REQ_URL = 'https://mdmcert.download/api/v1/signrequest'

# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'


@api_push_app.route('/v1/devices/<int:device_id>/push', methods=['POST', 'GET'])
def push(device_id: int):
    """Send a (Blank) push notification to the specified device by its Commandment ID.
    
    This causes the device to check back with the MDM for pending commands.

    :statuscode 400: impossible to push to device (no token or invalid token)
    :statuscode 404: device does not exist
    :statuscode 200: push complete
    """
    device = db.session.query(Device).filter(Device.id == device_id).one()
    if device.token is None or device.push_magic is None:
        abort(jsonify(error=True, message='Cannot request push on a device that has no device token or push magic'))

    try:
        response = push_to_device(device)
    except ssl.SSLError:
        return abort(jsonify(error=True, message="The push certificate has expired"))

    current_app.logger.info("[APNS2 Response] Status: %d, Reason: %s, APNS ID: %s, Timestamp",
                            response.status_code, response.reason, response.apns_id.decode('utf-8'))
    device.last_push_at = datetime.utcnow()
    if response.status_code == 200:
        device.last_apns_id = response.apns_id
        
    db.session.commit()
    push_res_schema = PushResponseFlatSchema()
    result = push_res_schema.dumps(response)

    return result
    

@api_push_app.route('/v1/push/certificate/public', methods=['POST'])
def upload_push_certificate_public():
    """Upload a push certificate pubkey to the MDM.

    The certificate is expected to be uploaded as multipart/form-data with the input name `file`.
    The format is expected to be PEM encoding.
    
    TODO: The reason for invalid certificate should be part of a json response

    :reqheader Accept: application/json
    :reqheader Content-Type: multipart/form-data
    :statuscode 204: no error
    :statuscode 400: invalid certificate supplied
    """
    if 'file' not in request.files:
        abort(400, 'no file uploaded in request data')

    f = request.files['file']

    # try to guess the upload Content-Type
    if f.content_type == 'application/x-x509-ca-cert':
        current_app.logger.debug('decoding DER certificate')
        der_data = f.read()
        crypto_cert = serialization.from_der(der_data)

    elif f.content_type == 'application/x-pem-data':
        current_app.logger.debug('decoding PEM certificate')
        pem_data = f.read()
        crypto_cert = serialization.from_pem(pem_data)
        
    else:
        abort(400, 'cannot determine certificate encoding type')

    try:
        c = db.session.query(Certificate).filter(Certificate.cert_type == 'mdm.pushcert').one()
    except NoResultFound:
        c = Certificate(cert_type='mdm.pushcert')

    c.subject = crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    c.not_before = crypto_cert.not_valid_before
    c.not_after = crypto_cert.not_valid_after
    c.fingerprint = crypto_cert.fingerprint(hashes.SHA256())
    c.pem_certificate = serialization.to_pem(crypto_cert)

    db.session.add(c)
    db.session.commit()

    return 'Success', 204, None


@api_push_app.route('/v1/push/certificate/private', methods=['POST'])
def upload_push_certificate_private():
    """Upload a push certificate pubkey to the MDM.
    
    The type of certificate encoding will be guessed from the Content-Type header in the request.
    
    TODO: The reason for invalid certificate should be part of a json response

    :reqheader Accept: application/json
    :reqheader Content-Type: application/pkcs8
    :statuscode 204: no error
    :statuscode 400: invalid certificate supplied
    """
    if request.headers['Content-Type'] not in ['application/x-pem-file', 'application/pkcs8']:
        abort(400, 'Invalid Content-Type supplied for private key')

    if request.headers['Content-Type'] == 'application/x-pem-file':
        pk = RSAPrivateKey(
            pem_key=request.data
        )
    else:
        crypto_key = serialization.rsa_from_der(request.data)
        pk = RSAPrivateKey(
            pem_key=serialization.rsa_to_pem(crypto_key)
        )

    db.session.add(pk)
    db.session.commit()

    return None, 204, None

#
# @api_push_app.route('/v1/push_certificate_data', methods=['GET'])
# def download_push_certificate():
#     """Download a push certificate from the MDM.
#
#     The type of certificate encoding will be guessed from the Accept header in the request.
#     Currently, only PEM encoded is supported.
#
#     :reqheader Accept: application/x-pem-file
#     :reqheader Accept: application/x-x509-user-cert
#     :reqheader Accept: application/x-x509-ca-cert
#     :resheader Content-Type: application/x-pem-file
#     :resheader Content-Type: application/x-x509-user-cert
#     :resheader Content-Type: application/x-x509-ca-cert
#     :statuscode 200: OK
#     :statuscode 404: There is no certificate configured
#     :statuscode 400: Can't produce requested encoding
#     """
#     c = db.session.query(Certificate).filter(Certificate.cert_type == 'mdm.pushcert').first()
#
#     if request.headers['Accept'] == 'application/x-pem-file':
#         bio = io.BytesIO(c.pem_certificate)
#         return send_file(bio, 'application/x-pem-file', True, 'push.pem')
#
#     elif request.headers['Accept'] == 'application/x-x509-user-cert':
#         cert = c.to_crypto()
#         serialized = cert.public_bytes(
#             encoding=serialization.Encoding.DER,
#             format=serialization.PublicFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         )
#         bio = io.BytesIO(serialized)
#         return send_file(bio, 'application/x-x509-user-cert', True, 'push.crt')
#     else:
#         abort(400, 'Certificate format not supported')

# elif request.headers['Accept'] == 'application/x-pkcs12':
#     cert = c.to_crypto()
#     return None


@api_push_app.route('/v1/mdmcert/request/<string:email>', methods=['GET'])
def mdmcert_request_csr(email: str):
    """Ask the mdmcert.download service to generate a new Certificate Signing Request for the given e-mail address.

    If an encryption certificate does not exist on the system, one will be generated to process the resulting encrypted
    and signed CSR.
    """
    try:
        apns_csr_model = db.session.query(CertificateSigningRequest).\
            filter(CertificateSigningRequest.x509_cn == "commandment-apns").one()
    except NoResultFound:
        private_key, csr = ssl.generate_signing_request('commandment-apns')
        private_key_model = RSAPrivateKey.from_crypto(private_key)
        db.session.add(private_key_model)
        apns_csr_model = CertificateSigningRequest.from_crypto(csr)
        db.session.add(apns_csr_model)
        db.session.commit()

    try:
        encrypt_cert_model = db.session.query(EncryptionCertificate).\
            filter(EncryptionCertificate.x509_cn == 'MDMCERT-DECRYPT').one()
    except NoResultFound:
        encrypt_key, encrypt_with_cert = ssl.generate_self_signed_certificate('MDMCERT-DECRYPT')
        encrypt_key_model = RSAPrivateKey.from_crypto(encrypt_key)
        db.session.add(encrypt_key_model)
        encrypt_cert_model = EncryptionCertificate.from_crypto(encrypt_with_cert)
        db.session.add(encrypt_cert_model)
        db.session.commit()

    mdmcert_result = submit_mdmcert_request(
        email=email,
        csr_pem=apns_csr_model.pem_data,
        encrypt_with_pem=encrypt_cert_model.pem_data,
    )

    return jsonify(mdmcert_result)


@api_push_app.route('/v1/mdmcert/signed_request', methods=['POST'])
def mdmcert_signed_request():
    """Upload the encrypted, signed request from mdmcert.download that was received via e-mail.

    The filename looks something like :file:`mdm_signed_request.YYMMDD_HHMMSS_NNN.plist.b64.p7`

    :reqheader Accept: application/json
    :reqheader Content-Type: multipart/form-data
    :statuscode 204: no error
    :statuscode 400: invalid or no certificate supplied
    """
    if 'file' not in request.files:
        return abort(400, 'no file uploaded in request data')

    f = request.files['file']

    return 'Success', 204, None
