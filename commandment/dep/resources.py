from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from .schema import DEPProfileSchema, DEPAccountSchema
from .models import db, DEPProfile, DEPAccount


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


class DEPAccountList(ResourceList):
    schema = DEPAccountSchema
    data_layer = {
        'session': db.session,
        'model': DEPAccount,
    }


class DEPAccountDetail(ResourceDetail):
    schema = DEPAccountSchema
    data_layer = {
        'session': db.session,
        'model': DEPAccount,
        'url_field': 'dep_account_id'
    }
