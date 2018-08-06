from datetime import datetime
from flask import Blueprint, request, abort, send_file, current_app, jsonify
from sqlalchemy.orm.exc import NoResultFound


from base64 import b64encode
from commandment.models import db, Device
from commandment.pki.models import Certificate, RSAPrivateKey, CertificateSigningRequest, CACertificate, \
    EncryptionCertificate
from commandment.pki import serialization, ssl as cmdssl
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from .push import push_to_device
from .schema import PushResponseFlatSchema
from .mdmcert import submit_mdmcert_request, decrypt_mdmcert
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


@api_push_app.route('/v1/mdmcert/request/<string:email>', methods=['GET'])
def mdmcert_request(email: str):
    """Ask the mdmcert.download service to generate a new Certificate Signing Request for the given e-mail address.

    If an encryption certificate does not exist on the system, one will be generated to process the resulting encrypted
    and signed CSR. The common name of the certificate will be the e-mail address that is registered with the
    mdmcert.download service, and the type will be an EncryptionCertificate.

    :reqheader Accept: application/json
    :resheader Content-Type: application/json
    """
    try:
        apns_csr_model = db.session.query(CertificateSigningRequest).\
            filter(CertificateSigningRequest.x509_cn == "commandment-apns").one()
    except NoResultFound:
        private_key, csr = cmdssl.generate_signing_request('commandment-apns')
        private_key_model = RSAPrivateKey.from_crypto(private_key)
        db.session.add(private_key_model)
        apns_csr_model = CertificateSigningRequest.from_crypto(csr)
        apns_csr_model.rsa_private_key = private_key_model
        db.session.add(apns_csr_model)
        db.session.commit()

    try:
        encrypt_cert_model = db.session.query(EncryptionCertificate).\
            filter(EncryptionCertificate.x509_cn == email).one()
    except NoResultFound:
        encrypt_key, encrypt_with_cert = cmdssl.generate_self_signed_certificate(email)
        encrypt_key_model = RSAPrivateKey.from_crypto(encrypt_key)
        db.session.add(encrypt_key_model)
        encrypt_cert_model = EncryptionCertificate.from_crypto(encrypt_with_cert)
        encrypt_cert_model.rsa_private_key = encrypt_key_model
        db.session.add(encrypt_cert_model)
        db.session.commit()

    current_app.logger.info("Submitting request to mdmcert.download for %s", email)
    mdmcert_result = submit_mdmcert_request(
        email=email,
        csr_pem=apns_csr_model.pem_data,
        encrypt_with_pem=encrypt_cert_model.pem_data,
    )

    return jsonify(mdmcert_result)


@api_push_app.route('/v1/mdmcert/decrypt', methods=['POST'])
def mdmcert_decrypt():
    """Upload the encrypted, signed request from mdmcert.download that was received via e-mail.

    The filename looks something like :file:`mdm_signed_request.YYMMDD_HHMMSS_NNN.plist.b64.p7`
    It is a hex-encoded PKCS#7 message.

    :reqheader Accept: application/json
    :reqheader Content-Type: multipart/form-data
    :statuscode 200: successfully decrypted request
    :statuscode 415: invalid or no certificate supplied
    :statuscode 501: impossible to serve the request because we don't have the matching key
    """
    if 'file' not in request.files:
        return abort(415, 'no file uploaded in request data')

    encrypted_payload = request.files['file'].stream.read()

    try:
        # TODO: Identify the specific certificate used to generate the request
        encrypt_cert: EncryptionCertificate = db.session.query(EncryptionCertificate).first()
    except NoResultFound:
        return abort(500, 'unable to decrypt, there was no decryption cert')

    pk = encrypt_cert.rsa_private_key.to_crypto()
    result = decrypt_mdmcert(encrypted_payload, pk)

    return 'B64CONTENT', 200, {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': 'attachment; filename=mdm_signed_request.%s.plist.b64' % datetime.now().strftime('%Y%m%d_%H%M%S'),
    }

