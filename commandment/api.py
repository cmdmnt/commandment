from flask import Blueprint
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from .models import db, Device, Certificate, CertificateSigningRequest, RSAPrivateKey, PushCertificate, CACertificate
from .api_schema import DeviceSchema, CertificateSchema, CertificateSigningRequestSchema, PrivateKeySchema


api_app = Blueprint('api_app', __name__)


class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


class CertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateTypeDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate, 'url_field': 'purpose', 'id_field': 'cert_type'}


class PrivateKeyDetail(ResourceDetail):
    schema = PrivateKeySchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateSigningRequestList(ResourceList):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest,
    }


class CertificateSigningRequestDetail(ResourceDetail):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest
    }


class PushCertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': PushCertificate
    }


class SSLCertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': Certificate
    }


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

api.route(PushCertificateList, 'push_certificates_list', '/v1/push_certificates')
api.route(SSLCertificateDetail, 'ssl_certificate_detail', '/v1/ssl_certificate')


