from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.models import db
from commandment.profiles.models import Profile
from commandment.profiles.schema import ProfileSchema


class ProfilesList(ResourceList):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile
    }


class ProfileDetail(ResourceDetail):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile,
        'url_field': 'profile_id'
    }


class ProfileRelationship(ResourceRelationship):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile,
        'url_field': 'profile_id'
    }
