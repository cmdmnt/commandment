from flask import url_for
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from .schema import DEPProfileSchema, DEPAccountSchema
from .models import db, DEPProfile, DEPAccount


class DEPProfileList(ResourceList):
    schema = DEPProfileSchema
    data_layer = {
        'session': db.session,
        'model': DEPProfile,
    }

    def before_post(self, args, kwargs, data=None):
        """Generate an MDM enrollment URL if none was given."""
        if 'url' not in data or data['url'] is None:
            data['url'] = url_for('dep_app.profile', _external=True)


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
