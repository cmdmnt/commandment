from datetime import datetime
import requests
import json
from flask import Blueprint, request, abort, send_file, current_app, jsonify
from sqlalchemy.orm.exc import NoResultFound

from base64 import b64encode
from commandment.models import db, Device, Certificate, RSAPrivateKey, CertificateSigningRequest, CACertificate
from commandment.pki import serialization, ssl
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from .push import push_to_device
from .schema import PushResponseFlatSchema
from .mdmcert import submit_mdmcert_request

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
        abort(400, 'Cannot request push on a device that has no device token or push magic')

    response = push_to_device(device)
    current_app.logger.info(response)
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


@api_push_app.route('/v1/push/certificate/generate_csr', methods=['GET'])
def generate_push_certificate_csr():
    """Generate a signed push certificate for upload to the Apple Push Certificate Portal.

    :resheader Content-Type: application/x-pem-file
    :resheader Content-Type: application/x-x509-user-cert
    :resheader Content-Type: application/x-x509-ca-cert
    """
    private_key, csr = ssl.generate_signing_request('commandment')
    private_key_model = RSAPrivateKey.from_crypto(private_key)
    db.session.add(private_key_model)
    csr_model = CertificateSigningRequest.from_crypto(csr)
    db.session.add(csr_model)

    encrypt_with = db.session.query(CACertificate).filter_by(x509_cn='COMMANDMENT-CA').one()

    base64_csr = b64encode(csr_model.pem_data)
    base64_recipient = b64encode(encrypt_with.pem_data)

    mdmcert_dict = {
        'csr': base64_csr.decode('utf8'),
        'email': 'cmdmnt@users.noreply.github.com',
        'key': MDMCERT_API_KEY,
        'encrypt': base64_recipient.decode('utf8'),
    }

    # return jsonify(mdmcert_dict)
    # res = requests.post(MDMCERT_REQ_URL, json=mdmcert_dict, headers={'User-Agent': 'coMmanDMent/0.1'})
    # return res.json()

    # req = urllib.request.Request(
    #     MDMCERT_REQ_URL,
    #     json.dumps(mdmcert_dict).encode('utf8'),
    #     {'Content-Type': 'application/json',
    #      'User-Agent': 'coMmanDMent/0.1'})
    #
    # f = urllib.request.urlopen(req)
    # resp = f.read()
    # f.close()
    #
    # return json.loads(resp)
