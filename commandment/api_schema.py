from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields


class DeviceSchema(Schema):
    class Meta:
        type_ = 'devices'
        self_view = 'device_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'device_list'

    id = fields.Str(dump_only=True)
    name = fields.Str()


class CertificateSchema(Schema):
    class Meta:
        type_ = 'certificates'
        self_view = 'certificate_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'certificate_list'

    id = fields.Str(dump_only=True)
    name = fields.Str()


class PushCertificateSchema(Schema):
    class Meta:
        type_ = 'push_certificates'
        self_view = 'push_certificate_detail'
        self_view_kwargs = {}

    id = fields.Int(dump_only=True)
    subject = fields.Str()
    not_before = fields.DateTime()
    not_after = fields.DateTime()


class CertificateSigningRequestSchema(Schema):
    class Meta:
        type_ = 'certificate_signing_requests'
        self_view = 'certificate_signing_request_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'certificate_signing_request_list'

    id = fields.Str(dump_only=True)
    purpose = fields.Str(load_only=True, attribute='req_type')
    subject = fields.Str(dump_only=True)
