from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import Schema as FlatSchema, post_load


class ApplicationManifestSchema(Schema):
    class Meta:
        type_ = 'application_manifests'
        self_view = 'applications_api.application_manifest_detail'
        self_view_kwargs = {'application_manifest_id': '<id>'}
        self_view_many = 'applications_api.application_manifest_list'
        strict = True


class ApplicationSchema(Schema):
    class Meta:
        type_ = 'applications'
        self_view = 'applications_api.application_detail'
        self_view_kwargs = {'application_id': '<id>'}
        self_view_many = 'applications_api.application_list'
        strict = True

    id = fields.Int(dump_only=True)
    display_name = fields.Str()
    description = fields.Str()
    manifest_url = fields.Url()

