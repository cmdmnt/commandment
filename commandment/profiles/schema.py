from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow import Schema as FlatSchema, post_load


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

