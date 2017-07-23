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
    device_name = fields.Str()
    model = fields.Str()
    model_name = fields.Str()
    os_version = fields.Str()
    product_name = fields.Str()
    serial_number = fields.Str()

    awaiting_configuration = fields.Bool()
    last_seen = fields.DateTime(dump_only=True)
    hostname = fields.Str()
    local_hostname = fields.Str()
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

    commands = Relationship(
        related_view='api_app.command_detail',
        related_view_kwargs={'command_id': '<id>'},
        many=True,
        schema='CommandSchema',
        type_='commands'
    )

    installed_certificates = Relationship(
        related_view='api_app.installed_certificate_detail',
        related_view_kwargs={'installed_certificate_id': '<id>'},
        many=True,
        schema='InstalledCertificateSchema',
        type_='installed_certificates'
    )

    installed_applications = Relationship(
        related_view='api_app.installed_application_detail',
        related_view_kwargs={'installed_application_id': '<id>'},
        many=True,
        schema='InstalledApplicationSchema',
        type_='installed_applications'
    )

    groups = Relationship(
        related_view='api_app.device_group_detail',
        related_view_kwargs={'device_group_id': '<id>'},
        many=True,
        schema='DeviceGroupSchema',
        type_='device_groups'
    )

    tags = Relationship(
        related_view='api_app.tag_detail',
        related_view_kwargs={'tag_id': '<id>'},
        many=True,
        schema='TagSchema',
        type_='tags'
    )



class DeviceGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

    devices = Relationship(
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        many=True,
        schema='DeviceSchema',
        type_='devices',
    )

    class Meta:
        type_ = 'device_groups'
        self_view = 'api_app.device_group_detail'
        self_view_kwargs = {'device_group_id': '<id>'}
        self_view_many = 'api_app.device_groups_list'
        strict = True


class CommandSchema(Schema):
    class Meta:
        type_ = 'commands'
        self_view = 'api_app.command_detail'
        self_view_kwargs = {'command_id': '<id>'}
        self_view_many = 'api_app.commands_list'
        strict = True

    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    request_type = fields.Str()
    status = fields.Str()
    queued_at = fields.DateTime()
    sent_at = fields.DateTime()
    acknowledged_at = fields.DateTime()
    after = fields.DateTime()
    ttl = fields.Int()

    device = Relationship(
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        type_='devices'
    )


class InstalledApplicationSchema(Schema):
    class Meta:
        type_ = 'installed_applications'
        self_view = 'api_app.installed_application_detail'
        self_view_kwargs = {'installed_application_id': '<id>'}
        self_view_many = 'api_app.installed_applications_list'
        strict = True
    
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
        related_view_kwargs={'device_id': '<device_id>'},
        type_='devices',
    )


class InstalledCertificateSchema(Schema):
    class Meta:
        type_ = 'installed_certificates'
        self_view = 'api_app.installed_certificate_detail'
        self_view_kwargs = {'installed_certificate_id': '<id>'}
        self_view_many = 'api_app.installed_certificates_list'
        strict = True

    id = fields.Int(dump_only=True)
    x509_cn = fields.Str(dump_only=True)
    is_identity = fields.Boolean(dump_only=True)
    fingerprint_sha256 = fields.String(dump_only=True)

    device = Relationship(
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        type_='devices',
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


class PushResponseFlatSchema(FlatSchema):
    """This structure mimics the fields of an APNS2 service reply."""
    apns_id = fields.Integer()
    status_code = fields.Integer()
    reason = fields.Str()
    timestamp = fields.DateTime()


class InstalledProfileSchema(Schema):
    class Meta:
        type_ = 'installed_profiles'
        self_view = 'api_app.installed_profile_detail'
        self_view_kwargs = {'installed_profile_id': '<id>'}
        self_view_many = 'api_app.installed_profiles_list'

    id = fields.Int(dump_only=True)

    has_removal_password = fields.Bool()
    is_encrypted = fields.Bool()
    payload_description = fields.Str()
    payload_display_name = fields.Str()
    payload_identifier = fields.Str()
    payload_organization = fields.Str()
    payload_removal_disallowed = fields.Boolean()
    payload_uuid = fields.UUID()
    # signer_certificates = fields.Nested()


class ProfileSchema(Schema):
    class Meta:
        type_ = 'profiles'
        self_view = 'api_app.profile_detail'
        self_view_kwargs = {'profile_id': '<id>'}
        self_view_many = 'api_app.profiles_list'

    id = fields.Int(dump_only=True)
    data = fields.String()

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

    tags = Relationship(
        related_view='api_app.tag_detail',
        related_view_kwargs={'tag_id': '<id>'},
        many=True,
        schema='TagSchema',
        type_='tags'
    )


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


class AvailableOSUpdateSchema(Schema):
    class Meta:
        type_ = 'available_os_updates'
        self_view = 'api_app.available_os_update_detail'
        self_view_kwargs = {'available_os_update_id': '<id>'}
        self_view_many = 'api_app.available_os_updates_list'

    id = fields.Int(dump_only=True)
    allows_install_later = fields.Boolean()
    #  app_identifiers_to_close = fields.List(fields.String())
    human_readable_name = fields.Str()
    human_readable_name_locale = fields.Str()
    is_config_data_update = fields.Boolean()
    is_critical = fields.Boolean()
    is_firmware_update = fields.Boolean()
    metadata_url = fields.URL()
    product_key = fields.String()
    restart_required = fields.Boolean()
    version = fields.String()
