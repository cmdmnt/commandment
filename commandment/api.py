from flask import Blueprint
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from .database import db_session
from .models import Device, Certificate, CertificateRequest, PrivateKey
from .extensions.datalayer import ExtendedSqlalchemyDataLayer
from .api_schema import DeviceSchema, CertificateSchema, CertificateSigningRequestSchema, PrivateKeySchema


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


class PrivateKeyDetail(ResourceDetail):
    schema = PrivateKeySchema
    data_layer = {'session': db_session, 'model': Certificate}

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
api.route(PrivateKeyDetail, 'private_key_detail', '/v1/private_keys/<int:private_key_id>')

api.route(PushCertificateDetail, 'push_certificate_detail', '/v1/push_certificate')
api.route(SSLCertificateDetail, 'ssl_certificate_detail', '/v1/ssl_certificate')


