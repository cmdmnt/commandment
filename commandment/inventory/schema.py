from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


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
        related_view_kwargs={'device_id': '<device_id>'},
        type_='devices',
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

