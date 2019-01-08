from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class ApplicationSchema(Schema):
    class Meta:
        type_ = 'applications'
        self_view = 'applications_api.application_detail'
        self_view_kwargs = {'application_id': '<id>'}
        self_view_many = 'applications_api.applications_list'
        strict = True

    id = fields.Int(dump_only=True)
    display_name = fields.Str()
    description = fields.Str()
    version = fields.Str()
    itunes_store_id = fields.Int()
    bundle_id = fields.Str()
    purchase_method = fields.Int()
    manifest_url = fields.Url()
    management_flags = fields.Int()
    change_management_state = fields.Str()

    # iTunes Search API cache
    country = fields.Str()
    artist_id = fields.Int()
    artist_name = fields.Str()
    artist_view_url = fields.Url()
    artwork_url60 = fields.Url()
    artwork_url100 = fields.Url()
    artwork_url512 = fields.Url()
    release_notes = fields.Str()
    release_date = fields.DateTime()
    minimum_os_version = fields.Str()
    file_size_bytes = fields.Number()

    tags = Relationship(
        related_view='api_app.tags_list',
        related_view_kwargs={'application_id': '<id>'},
        many=True,
        schema='TagSchema',
        type_='tags'
    )


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

