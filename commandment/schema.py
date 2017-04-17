from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import Schema as FlatSchema


class DeviceSchema(Schema):
    """marshmallow-jsonapi schema for Device objects."""
    id = fields.Int(dump_only=True)
    udid = fields.Str(dump_only=True)
    topic = fields.Str()

    build_version = fields.Str()
    device_name = fields.Str()
    model = fields.Str()
    model_name = fields.Str()
    os_version = fields.Str()
    product_name = fields.Str()
    serial_number = fields.Str()

    awaiting_configuration = fields.Bool()
    last_seen = fields.DateTime()
    hostname = fields.Str()
    local_hostname = fields.Str()
    available_device_capacity = fields.Int()
    device_capacity = fields.Int()
    wifi_mac = fields.Str()
    bluetooth_mac = fields.Str()

    # private
    # push_magic = fields.Str()
    # token = fields.Str()
    # unlock_token = fields.Str()

    # TODO: Relationship to dep_config

    # certificate = Relationship(
    #     self_view='api_app.device_certificate',
    #     self_view_kwargs={'certificate_id': '<id>'},
    #     related_view='api_app.certificate_detail',
    #     related_view_kwargs={'certificate_id': '<id>'},
    # )

    commands = Relationship(
        related_view='api_app.command_detail',
        related_view_kwargs={'command_id': '<id>'},
        many=True,
        schema='CommandSchema',
        type_='commands'
    )

    class Meta:
        type_ = 'devices'
        self_view = 'api_app.device_detail'
        self_view_kwargs = {'device_id': '<id>'}
        self_view_many = 'api_app.devices_list'
        strict = True


class CommandSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    request_type = fields.Str()
    status = fields.Str()
    queued_at = fields.DateTime()
    sent_at = fields.DateTime()
    acknowledged_at = fields.DateTime()
    after = fields.DateTime()
    ttl = fields.Int()


    # device = Relationship(
    #     related_view='api_app.device_detail',
    #     related_url_kwargs={'device_id': '<id>'},
    #     many=False,
    #     schema='DeviceSchema',
    #     type_='devices'
    # )

    class Meta:
        type_ = 'commands'
        self_view = 'api_app.command_detail'
        self_view_kwargs = {'command_id': '<id>'}
        self_view_many = 'api_app.commands_list'
        strict = True


class InstalledApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    bundle_identifier = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    short_version = fields.Str(dump_only=True)
    version = fields.Str(dump_only=True)
    bundle_size = fields.Int(dump_only=True)
    dynamic_size = fields.Int(dump_only=True)
    is_validated = fields.Bool(dump_only=True)

    device = Relationship(
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        type_='devices',
    )

    class Meta:
        type_ = 'installed_applications'
        self_view = 'api_app.installed_application_detail'
        self_view_kwargs = {'installed_application_id': '<id>'}
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


class OrganizationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    payload_prefix = fields.Str()

    x509_ou = fields.Str()
    x509_o = fields.Str()
    x509_st = fields.Str()
    x509_c = fields.Str()

    class Meta:
        type_ = 'organizations'
        self_view = 'api_app.organization_detail'
        self_view_kwargs = {'organization_id': '<id>'}
        self_view_many = 'api_app.organizations_list'


class OrganizationFlatSchema(FlatSchema):
    name = fields.Str(required=True)
    payload_prefix = fields.Str(required=True)

    x509_ou = fields.Str()
    x509_o = fields.Str()
    x509_st = fields.Str()
    x509_c = fields.Str()


class PushResponseFlatSchema(FlatSchema):
    apns_id = fields.Integer()
    status_code = fields.Integer()
    reason = fields.Str()
    timestamp = fields.DateTime()


class ProfileSchema(Schema):
    """marshmallow-jsonapi schema for Profile SQLAlchemy models."""
    id = fields.Int(dump_only=True)
    description = fields.Str()
    display_name = fields.Str()
    expiration_date = fields.DateTime()
    identifier = fields.Str()
    organization = fields.Str()
    uuid = fields.UUID()
    removal_disallowed = fields.Boolean()
    version = fields.Int()
    scope = fields.Str()
    removal_date = fields.DateTime()
    duration_until_removal = fields.Int()
    consent_en = fields.Str()

    payloads = Relationship(
        related_view='api_app.payload_detail',
        related_view_kwargs={'payload_id': '<id>'},
        type_='payloads',
    )

    class Meta:
        type_ = 'profiles'
        self_view = 'api_app.profile_detail'
        self_view_kwargs = {'profile_id': '<id>'}
        self_view_many = 'api_app.profiles_list'
