from flask import Blueprint, current_app, app, request, abort, g
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
import json

from .decorators import pem_certificate_upload
from .database import db_session
from .models import Device, Certificate as DBCertificate, CertificateRequest as DBCSR
from .push import push_to_device
from .extensions.datalayer import ExtendedSqlalchemyDataLayer

api_app = Blueprint('api_app', __name__)


# Schemas

class DeviceSchema(Schema):
    class Meta:
        type_ = 'device'
        self_view = 'device_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'device_list'

    id = fields.Str(dump_only=True)
    name = fields.Str()


class CertificateSchema(Schema):
    class Meta:
        type_ = 'certificate'
        self_view = 'certificate_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'certificate_list'

    id = fields.Str(dump_only=True)
    name = fields.Str()


class PushCertificateSchema(Schema):
    class Meta:
        type_ = 'push_certificate'
        self_view = 'push_certificate_detail'
        self_view_kwargs = {}

    id = fields.Int(dump_only=True)
    subject = fields.Str()
    not_before = fields.DateTime()
    not_after = fields.DateTime()


class CertificateSigningRequestSchema(Schema):
    class Meta:
        type_ = 'certificate_signing_request'
        self_view = 'certificate_signing_request_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'certificate_signing_request_list'

    id = fields.Str(dump_only=True)
    purpose = fields.Str(load_only=True, attribute='req_type')
    subject = fields.Str(dump_only=True)


# Resource Managers

class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db_session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {'session': db_session,
                  'model': Device}


class CertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {'session': db_session, 'model': DBCertificate}


class CertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db_session, 'model': DBCertificate}


class CertificateSigningRequestList(ResourceList):
    schema = CertificateSigningRequestSchema
    data_layer = {'session': db_session, 'model': DBCSR}


class CertificateSigningRequestDetail(ResourceDetail):
    schema = CertificateSigningRequestSchema
    data_layer = {'session': db_session, 'model': DBCSR}


class PushCertificateDetail(ResourceDetail):

    def query(self, view_kwargs):
        query_ = self.session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.pushcert')
        return query_
    
    schema = PushCertificateSchema
    data_layer = {
        'class': ExtendedSqlalchemyDataLayer,
        'session': db_session, 'model': DBCertificate, 'methods': {'query': query}}
    methods = ['GET']
    is_singleton = True




api = Api(api_app)
api.route(DeviceList, 'device_list', '/v1/devices')
api.route(DeviceDetail, 'device_detail', '/v1/devices/<int:id>')
api.route(CertificateList, 'certificate_list', '/v1/certificates')
api.route(CertificateDetail, 'certificate_detail', '/v1/certificates/<int:id>')
api.route(CertificateSigningRequestList, 'certificate_signing_request_list', '/v1/certificate_signing_requests')
api.route(CertificateSigningRequestDetail, 'certificate_signing_request_detail',
          '/v1/certificate_signing_requests/<int:id>')
api.route(PushCertificateDetail, 'push_certificate_detail', '/v1/push_certificate')


@api_app.route('/v1/devices/<int:device_id>/push')
def push(device_id: int):
    device = db_session.query(Device).filter(Device.id == device_id).one()
    push_to_device(device)


@api_app.route('/v1/push.p12', methods=['POST'])
def post_push_pkcs12():
    """Upload a push certificate to the MDM in PKCS#12 format.

    :reqheader Accept: application/x-pkcs12
    :resheader Content-Type: application/json
    :statuscode 204: no error
    :statuscode 400: invalid certificate supplied
    """
    if 'file' not in request.files:
        abort(400, 'No certificate supplied in request')

    certificate_data = request.files['file']

    from asn1crypto.core import Sequence
    from asn1crypto.pkcs12 import Pfx, SafeBag
    parsed = Pfx.load(certificate_data.read())
    parsed.debug()
    # TODO: support PKCS#12


@api_app.route('/v1/push.pem', methods=['POST'])
@pem_certificate_upload
def post_push_pem():
    """Upload a push certificate to the MDM in PEM format.

    :reqheader Accept: application/x-pem-file
    :resheader Content-Type: application/json
    :statuscode 204: no error
    :statuscode 400: invalid certificate supplied
    """
    certificate = g.certificate
    db_cert = DBCertificate.from_crypto(certificate, 'mdm.pushcert')
    db_session.add(db_cert)
    db_session.commit()

    return json.dumps({'created': True}), 201, None

# @api_app.route('/v1/certificates/<int:certificate_id>', methods=['GET', 'PUT'])
# def certificate(certificate_id: int):
#     cert = db_session.query(DBCertificate).filter(DBCertificate.id == certificate_id).one()
#
#     if request.method == 'GET':
#         return cert.pem_certificate, 200, {'Content-Type': 'application/x-pem-file'}
#     else:
#         cert.pem_certificate = request.form['data']
#         cert.commit()
#
#         return None, 202
