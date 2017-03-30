from flask import Blueprint, request, abort, send_file, current_app
from sqlalchemy.orm.exc import NoResultFound

from .database import db_session
from .models import Device, Certificate, PrivateKey
from .pki import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

api_push_app = Blueprint('api_push_app', __name__)


# @api_push_app.route('/v1/devices/<int:device_id>/push', methods=['POST'])
# def push(device_id: int):
#     """Send a (Blank) push to the specified device by its ID"""
#     device = db_session.query(Device).filter(Device.id == device_id).one()
#     push_to_device(device)

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
        c = db_session.query(Certificate).filter(Certificate.cert_type == 'mdm.pushcert').one()
    except NoResultFound:
        c = Certificate(cert_type='mdm.pushcert')

    c.subject = crypto_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    c.not_before = crypto_cert.not_valid_before
    c.not_after = crypto_cert.not_valid_after
    c.fingerprint = crypto_cert.fingerprint(hashes.SHA256())
    c.pem_certificate = serialization.to_pem(crypto_cert)

    db_session.add(c)
    db_session.commit()

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
        pk = PrivateKey(
            pem_key=request.data
        )
    else:
        crypto_key = serialization.rsa_from_der(request.data)
        pk = PrivateKey(
            pem_key=serialization.rsa_to_pem(crypto_key)
        )

    db_session.add(pk)
    db_session.commit()

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
#     c = db_session.query(Certificate).filter(Certificate.cert_type == 'mdm.pushcert').first()
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
