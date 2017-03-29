from flask import Blueprint, current_app, app, request, abort, g, send_file
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList

import json
import io

from .decorators import pem_certificate_upload
from .database import db_session
from .models import Device, Certificate, CertificateRequest, PrivateKey
from .push import push_to_device
from .extensions.datalayer import ExtendedSqlalchemyDataLayer
from .api_schema import DeviceSchema, CertificateSchema, CertificateSigningRequestSchema

api_app = Blueprint('api_app', __name__)


class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db_session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {'session': db_session, 'model': Device}


class CertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {'session': db_session, 'model': Certificate}


class CertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db_session, 'model': Certificate}


class CertificateTypeDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db_session, 'model': Certificate, 'url_field': 'purpose', 'id_field': 'cert_type'}


class CertificateSigningRequestList(ResourceList):

    def before_create_object(self, data, view_kwargs):
        """
        :param dict data: the data validated by marshmallow
        :param dict view_kwargs: kwargs from the resource view 
        :return:
        """
        pass
        # pk, csr = CertificateRequest.generate()
        # commit pk
        # data['pem_request'] = csr as pem


    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db_session,
        'model': CertificateRequest,
        'methods': {
            'before_create_object': before_create_object
        }
    }




class CertificateSigningRequestDetail(ResourceDetail):
    schema = CertificateSigningRequestSchema
    data_layer = {'session': db_session, 'model': CertificateRequest}


class PushCertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {
        'class': ExtendedSqlalchemyDataLayer,
        'session': db_session, 'model': Certificate,
        'is_singleton': True}


class SSLCertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {
        'class': ExtendedSqlalchemyDataLayer,
        'session': db_session, 'model': Certificate,
        'is_singleton': True}


api = Api(api_app)
api.route(DeviceList, 'device_list', '/v1/devices')
api.route(DeviceDetail, 'device_detail', '/v1/devices/<int:device_id>')
api.route(CertificatesList, 'certificates_list', '/v1/certificates/')
api.route(CertificateDetail, 'certificate_detail', '/v1/certificates/<int:certificate_id>')
api.route(CertificateTypeDetail, 'certificate_type_detail', '/v1/certificates/type/<string:purpose>')
api.route(CertificateSigningRequestList, 'certificate_signing_request_list', '/v1/certificate_signing_requests')
api.route(CertificateSigningRequestDetail, 'certificate_signing_request_detail',
          '/v1/certificate_signing_requests/<int:certificate_signing_request_id>')

api.route(PushCertificateDetail, 'push_certificate_detail', '/v1/push_certificate')
api.route(SSLCertificateDetail, 'ssl_certificate_detail', '/v1/ssl_certificate')


@api_app.route('/v1/devices/<int:device_id>/push', methods=['POST'])
def push(device_id: int):
    """Send a (Blank) push to the specified device by its ID"""
    device = db_session.query(Device).filter(Device.id == device_id).one()
    push_to_device(device)


@api_app.route('/v1/push_certificate_data', methods=['POST'])
@pem_certificate_upload
def upload_push_certificate():
    """Upload a push certificate to the MDM.
    
    The type of certificate encoding will be guessed from the Content-Type header in the request.
    Currently, only PEM encoded is supported.
    
    TODO: The reason for invalid certificate should be part of a json response

    :reqheader Accept: application/json
    :reqheader Content-Type: application/x-pem-file 
    :reqheader Content-Type: application/x-x509-user-cert 
    :reqheader Content-Type: application/x-x509-ca-cert
    :statuscode 204: no error
    :statuscode 400: invalid certificate supplied
    """
    certificate = g.certificate
    db_cert = Certificate.from_crypto(certificate, 'mdm.pushcert')
    db_session.add(db_cert)
    db_session.commit()

    return json.dumps({'created': True}), 201, None


@api_app.route('/v1/push_certificate_data', methods=['GET'])
def download_push_certificate():
    """Download a push certificate from the MDM.
    
    The type of certificate encoding will be guessed from the Accept header in the request.
    Currently, only PEM encoded is supported.

    :reqheader Accept: application/x-pem-file
    :reqheader Accept: application/x-x509-user-cert
    :reqheader Accept: application/x-x509-ca-cert
    :resheader Content-Type: application/x-pem-file 
    :resheader Content-Type: application/x-x509-user-cert 
    :resheader Content-Type: application/x-x509-ca-cert
    :statuscode 200: OK
    :statuscode 404: There is no certificate configured
    :statuscode 400: Can't produce requested encoding
    """
    c = db_session.query(Certificate).filter(Certificate.cert_type == 'mdm.pushcert').first()
    bio = io.BytesIO(c.pem_certificate)
    # return c.pem_certificate, 200, {'Content-Type': 'application/x-pem-file'}
    return send_file(bio, 'application/x-pem-file', True, 'push.pem')

