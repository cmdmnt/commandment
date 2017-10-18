from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import Schema as FlatSchema, post_load


class ApplicationManifestSchema(Schema):
    class Meta:
        type_ = 'application_manifests'
        self_view = 'api_app.application_manifest_detail'
        self_view_kwargs = {'application_manifest_id': '<id>'}
        self_view_many = 'api_app.application_manifest_list'
        strict = True
