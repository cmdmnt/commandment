from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class DeviceSchema(Schema):
    """marshmallow-jsonapi schema for Device objects."""
    id = fields.Int(dump_only=True)
    udid = fields.Str(dump_only=True)
    push_magic = fields.Str()
    token = fields.Str()
    unlock_token = fields.Str()
    topic = fields.Str()
    serial_number = fields.Str()

    # TODO: Relationship to dep_config

    certificate = Relationship(
        self_view='api_app.device_certificate',
        self_view_kwargs={'certificate_id': '<id>'},
        related_view='api_app.certificate_detail',
        related_view_kwargs={'certificate_id': '<id>'},
    )

    class Meta:
        type_ = 'devices'
        self_view = 'api_app.device_detail'
        self_view_kwargs = {'device_id': '<id>'}
        self_view_many = 'api_app.devices_list'
        strict = True


class PrivateKeySchema(Schema):
    id = fields.Int(dump_only=True)
    pem_key = fields.Str()

    class Meta:
        type_ = 'private_keys'
        self_view = 'api_app.private_key_detail'
        self_view_kwargs = {'private_key_id': '<id>'}
        strict = True
    

class CertificateSchema(Schema):
    """marshmallow-jsonapi schema for Certificate objects."""
    id = fields.Int(dump_only=True)
    type = fields.Str(attribute='type')
    x509_cn = fields.Str(dump_only=True)
    not_before = fields.DateTime(dump_only=True)
    not_after = fields.DateTime(dump_only=True)
    # fingerprint = fields.Str(dump_only=True)
    pem_certificate = fields.Str()

    private_key = Relationship(
        self_view='api_app.certificate_private_keys',
        self_view_kwargs={'id': '<id>'},
        related_view='api_app.private_key_detail',
        related_view_kwargs={'private_key_id': '<id>'},
        many=False,
        schema='PrivateKeySchema',
        type_='private_keys'
    )

    class Meta:
        type_ = 'certificates'
        self_view = 'api_app.certificate_detail'
        self_view_kwargs = {'certificate_id': '<id>'}
        self_view_many = 'api_app.certificates_list'
        strict = True


class CertificateSigningRequestSchema(Schema):
    """marshmallow-jsonapi schema for CertificateRequest objects."""
    id = fields.Int(dump_only=True)
    purpose = fields.Str(load_only=True, attribute='req_type')
    subject = fields.Str()
    pem_request = fields.Str()

    class Meta:
        type_ = 'certificate_signing_requests'
        self_view = 'api_app.certificate_signing_request_detail'
        self_view_kwargs = {'certificate_signing_request_id': '<id>'}
        self_view_many = 'api_app.certificate_signing_request_list'
