from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ApplicationSchema(Schema):
    class Meta:
        type_ = 'applications'
        self_view = 'applications_api.application_detail'
        self_view_kwargs = {'application_id': '<id>'}
        self_view_many = 'applications_api.application_list'
        strict = True

    id = fields.Int(dump_only=True)
    manifest_url = fields.Url()


class ApplicationManifestSchema(Schema):
    class Meta:
        type_ = 'application_manifests'
        self_view = 'applications_api.application_manifest_detail'
        self_view_kwargs = {'application_manifest_id': '<id>'}
        self_view_many = 'applications_api.application_manifest_list'
        strict = True

    checksums = Relationship(
        related_view='applications_api.application_manifest_checksum_detail',
        related_view_kwargs={'application_checksum_id': '<id>'},
        many=True,
        schema='ApplicationManifestChecksumSchema',
        type_='application_manifest_checksums'
    )

    full_size_image_url = fields.Url()
    display_image_url = fields.Url()


class ApplicationManifestChecksumSchema(Schema):
    class Meta:
        type_ = 'application_manifest_checksums'
        self_view = 'applications_api.application_manifest_checksum_detail'
        self_view_kwargs = {'application_checksum_id': '<id>'}
        self_view_many = 'applications_api.application_manifest_checksum_list'
        strict = True

