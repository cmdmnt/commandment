"""
    This module contains schema definitions for Marshmallow-JSONAPI and therefore Flask-REST-JSONAPI.
    It also contains non subpackage specific JSON schema definitions.
"""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import Schema as FlatSchema, post_load
from commandment.models import db, Organization, SCEPConfig


class DeviceSchema(Schema):
    class Meta:
        type_ = 'devices'
        self_view = 'api_app.device_detail'
        self_view_kwargs = {'device_id': '<id>'}
        self_view_many = 'api_app.devices_list'
        strict = True

    id = fields.Int(dump_only=True)
    udid = fields.Str(dump_only=True)
    topic = fields.Str()

    build_version = fields.Str()

    # device_name and hostname are "pseudo" read-only in that writing them does not affect the field but enqueues
    # an MDM command to change the name.
    device_name = fields.Str()
    hostname = fields.Str()
    local_hostname = fields.Str(dump_only=True)

    model = fields.Str()
    model_name = fields.Str()
    os_version = fields.Str()
    product_name = fields.Str()
    serial_number = fields.Str()

    awaiting_configuration = fields.Bool()
    last_seen = fields.DateTime(dump_only=True)

    available_device_capacity = fields.Float()
    device_capacity = fields.Float()
    wifi_mac = fields.Str()
    bluetooth_mac = fields.Str()

    # private
    # push_magic = fields.Str()
    # token = fields.Str()
    # unlock_token = fields.Str()
    tokenupdate_at = fields.DateTime()

    # SecurityInfo
    passcode_present = fields.Bool()
    passcode_compliant = fields.Bool()
    passcode_compliant_with_profiles = fields.Bool()
    fde_enabled = fields.Bool()
    fde_has_prk = fields.Bool()
    fde_has_irk = fields.Bool()
    firewall_enabled = fields.Bool()
    block_all_incoming = fields.Bool()
    stealth_mode_enabled = fields.Bool()
    sip_enabled = fields.Bool()

    # TODO: Relationship to dep_config

    # certificate = Relationship(
    #     self_view='api_app.device_certificate',
    #     self_view_kwargs={'certificate_id': '<id>'},
    #     related_view='api_app.certificate_detail',
    #     related_view_kwargs={'certificate_id': '<id>'},
    # )

    # DEP
    is_dep = fields.Bool()
    description = fields.Str(dump_only=True)
    color = fields.Str(dump_only=True)
    asset_tag = fields.Str(dump_only=True)
    profile_status = fields.Str(dump_only=True)
    profile_uuid = fields.UUID(dump_only=True)
    profile_assign_time = fields.DateTime(dump_only=True)
    profile_push_time = fields.DateTime(dump_only=True)
    device_assigned_date = fields.DateTime(dump_only=True)
    device_assigned_by = fields.Str(dump_only=True)
    os = fields.Str(dump_only=True)
    device_family = fields.Str(dump_only=True)

    commands = Relationship(
        related_view='api_app.commands_list',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='CommandSchema',
        type_='commands'
    )

    installed_certificates = Relationship(
        related_view='api_app.installed_certificates_list',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='InstalledCertificateSchema',
        type_='installed_certificates'
    )

    installed_applications = Relationship(
        related_view='api_app.installed_applications_list',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='InstalledApplicationSchema',
        type_='installed_applications'
    )

    tags = Relationship(
        related_view='api_app.tags_list',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='TagSchema',
        type_='tags'
    )

    available_os_updates = Relationship(
        related_view='api_app.available_os_updates_list',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='AvailableOSUpdateSchema',
        type_='available_os_updates'
    )

    dep_profile = Relationship(
        related_view='dep_app.dep_profile_detail',
        related_view_kwargs={'device_id': '<id>'},
        many=False,
        schema='DEPProfileSchema',
        type_='dep_profiles',
    )


class PrivateKeySchema(Schema):
    class Meta:
        type_ = 'private_keys'
        self_view = 'api_app.private_key_detail'
        self_view_kwargs = {'private_key_id': '<id>'}
        strict = True

    id = fields.Int(dump_only=True)
    pem_key = fields.Str()


class CertificateSchema(Schema):
    class Meta:
        type_ = 'certificates'
        self_view = 'api_app.certificate_detail'
        self_view_kwargs = {'certificate_id': '<id>'}
        self_view_many = 'api_app.certificates_list'
        strict = True

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


class CertificateSigningRequestSchema(Schema):
    class Meta:
        type_ = 'certificate_signing_requests'
        self_view = 'api_app.certificate_signing_request_detail'
        self_view_kwargs = {'certificate_signing_request_id': '<id>'}
        self_view_many = 'api_app.certificate_signing_request_list'

    id = fields.Int(dump_only=True)
    purpose = fields.Str(load_only=True, attribute='req_type')
    subject = fields.Str()
    pem_request = fields.Str()


class OrganizationSchema(Schema):
    class Meta:
        type_ = 'organizations'
        self_view = 'api_app.organization_detail'
        self_view_kwargs = {'organization_id': '<id>'}

    id = fields.Int(dump_only=True)
    name = fields.Str()
    payload_prefix = fields.Str()

    x509_ou = fields.Str()
    x509_o = fields.Str()
    x509_st = fields.Str()
    x509_c = fields.Str()


class OrganizationFlatSchema(FlatSchema):
    name = fields.Str(required=True)
    payload_prefix = fields.Str(required=True)

    x509_ou = fields.Str()
    x509_o = fields.Str()
    x509_st = fields.Str()
    x509_c = fields.Str()

    @post_load
    def make_organization(self, data: dict) -> Organization:
        """Construct a model from a parsed JSON schema."""
        rows = db.session.query(Organization).count()
        
        if rows == 1:
            db.session.query(Organization).update(data)
            o = db.session.query(Organization).first()
        else:
            o = Organization(**data)
            db.session.add(o)

        return o

    
class SCEPConfigFlatSchema(FlatSchema):
    source_type = fields.String()
    url = fields.Url(relative=False, schemes=['http', 'https'], required=True)
    challenge_enabled = fields.Boolean()
    ca_fingerprint = fields.String()
    subject = fields.String()
    key_size = fields.Integer()
    key_type = fields.String(dump_only=True)
    key_usage = fields.Integer()
    subject_alt_name = fields.String()
    retries = fields.Integer()
    retry_delay = fields.Integer()
    certificate_renewal_time_interval = fields.Integer()

    @post_load
    def make_scepconfig(self, data: dict) -> SCEPConfig:
        """Construct a model from a parsed JSON schema."""
        rows = db.session.query(SCEPConfig).count()

        if rows == 1:
            db.session.query(SCEPConfig).update(data)
            o = db.session.query(SCEPConfig).first()
        else:
            o = SCEPConfig(**data)
            db.session.add(o)

        return o




class TagSchema(Schema):
    class Meta:
        type_ = 'tags'
        self_view = 'api_app.tag_detail'
        self_view_kwargs = {'tag_id': '<id>'}
        self_view_many = 'api_app.tags_list'

    id = fields.Int(dump_only=True)
    name = fields.Str()
    color = fields.Str()

    devices = Relationship(
        self_view='api_app.tag_devices',
        self_view_kwargs={'tag_id': '<id>'},
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        schema='DeviceSchema',
        many=True,
        type_='devices'
    )

    # profiles = Relationship(
    #     related_view='api_app.profiles_list',
    #     related_view_kwargs={'profile_id': '<id>'},
    #     schema='ProfileSchema',
    #     many=True,
    #     type_='profiles'
    # )
