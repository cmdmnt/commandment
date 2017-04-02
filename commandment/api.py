import io
from flask import Blueprint, send_file
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from .models import db, Device, Certificate, CertificateSigningRequest, RSAPrivateKey, PushCertificate, CACertificate, \
    SSLCertificate, Organization
from .api_schema import DeviceSchema, CertificateSchema, CertificateSigningRequestSchema, PrivateKeySchema, OrganizationSchema

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


class CACertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': CACertificate
    }


class SSLCertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': SSLCertificate
    }


class OrganizationList(ResourceList):
    schema = OrganizationSchema
    data_layer = {
        'session': db.session,
        'model': Organization
    }

api = Api(api_app)

# Certificates
api.route(CertificatesList, 'certificates_list', '/v1/certificates/')
api.route(CertificateDetail, 'certificate_detail', '/v1/certificates/<int:certificate_id>')
api.route(CertificateTypeDetail, 'certificate_type_detail', '/v1/certificates/type/<string:purpose>')

api.route(CertificateSigningRequestList, 'certificate_signing_request_list', '/v1/certificate_signing_requests')
api.route(CertificateSigningRequestDetail, 'certificate_signing_request_detail',
          '/v1/certificate_signing_requests/<int:certificate_signing_request_id>')
api.route(PushCertificateList, 'push_certificates_list', '/v1/push_certificates')
api.route(SSLCertificatesList, 'ssl_certificates_list', '/v1/ssl_certificates')
api.route(CACertificateList, 'ca_certificates_list', '/v1/ca_certificates')
api.route(PrivateKeyDetail, 'private_key_detail', '/v1/private_keys/<int:private_key_id>')


@api_app.route('/v1/certificates/<int:certificate_id>/download')
def download_certificate(certificate_id: int):
    """Download a certificate in PEM format

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
    c = db.session.query(Certificate).filter(Certificate.id == certificate_id).one()
    bio = io.BytesIO(c.pem_data)

    return send_file(bio, 'application/x-pem-file', True, 'certificate.pem')

# Devices
api.route(DeviceList, 'device_list', '/v1/devices')
api.route(DeviceDetail, 'device_detail', '/v1/devices/<int:device_id>')

api.route(OrganizationList, 'organizations_list', '/v1/organizations')
