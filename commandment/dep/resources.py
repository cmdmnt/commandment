from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from .schema import DEPProfileSchema
from .models import db, DEPProfile


class DEPProfileList(ResourceList):
    schema = DEPProfileSchema
    data_layer = {
        'session': db.session,
        'model': DEPProfile,
    }


class DEPProfileDetail(ResourceDetail):
    schema = DEPProfileSchema
    data_layer = {
        'session': db.session,
        'model': DEPProfile,
        'url_field': 'dep_profile_id'
    }


class DEPProfileRelationship(ResourceRelationship):
    schema = DEPProfileSchema
    data_layer = {
        'session': db.session,
        'model': DEPProfile,
        'url_field': 'dep_profile_id'
    }
