'''
Copyright (c) 2016 Flax & Teal Limited
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, current_app
from flask.ext.restful import Api, Resource, reqparse
import json
from .models import Profile, MDMGroup
from .database import db_session
from .admin import install_group_profiles_to_device, remove_group_profiles_from_device
from .push import push_to_device


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('identifier')
parser.add_argument('uuid')
parser.add_argument('profile_data')
parser.add_argument('group_name')
parser.add_argument('groups')


class ProfileResource(Resource):
    fillable = ('identifier', 'uuid', 'profile_data')

    def __init__(self, *args, **kwargs):
        self.query = db_session.query(Profile)
        super(ProfileResource, self).__init__(*args, **kwargs)

    # Create
    def put(self):
        args = parser.parse_args()

        profile = Profile(*[args[x] for x in self.fillable if (x in args and args[x] is not None)])
        db_session.add(profile)

        if 'groups' in args and args['groups'] is not None:
            group_list = json.loads(args['groups']);
            profile.mdm_groups = [db_session.query(MDMGroup).get(g['id']) for g in group_list]

        db_session.commit()

        return {'id': profile.id}

    # Retrieve
    def get(self, id):
        profile = db_session.query(Profile).get(id)

        if not profile:
            return None, 404

        profile_dict = profile.as_dict()
        profile_dict['groups'] = [g.as_dict() for g in profile.mdm_groups]

        return profile_dict

    # Update
    def post(self, id):
        args = parser.parse_args()

        profile = db_session.query(Profile).get(id)
        if not profile:
            return None, 404

        profile.update(**{x: args[x] for x in self.fillable if (x in args and args[x] is not None)})

        if 'groups' in args and args['groups'] is not None:
            group_list = json.loads(args['groups']);
            print group_list
            profile.mdm_groups = [db_session.query(MDMGroup).get(g['id']) for g in group_list]

        db_session.commit()

    # Delete
    def delete(self, id):
        profile = db_session.query(Profile).get(id)
        db_session.delete(profile)

        db_session.commit()

class MDMGroupResource(Resource):
    fillable = ('group_name', 'description')

    # Create
    def put(self):
        args = parser.parse_args()

        group = MDMGroup(*[args[x] for x in self.fillable if (x in args and args[x] is not None)])
        db_session.add(group)

        db_session.commit()

        return {'id': group.id}

    # Retrieve
    def get(self, id=None):
        if id:
            mdm_group = db_session.query(MDMGroup).get(id)
            return mdm_group

        query = db_session.query(MDMGroup)
        args = {k: v for k, v in parser.parse_args().items() if k in self.fillable and v is not None}

        if args:
            query = query.filter_by(**args)

        return [g.as_dict() for g in query.all()]

    # Update
    def post(self, id):
        args = parser.parse_args()

        group = db_session.query(MDMGroup).get(id)
        if not group:
            return None, 404

        group.update(**{x: args[x] for x in self.fillable if (x in args and args[x] is not None)})

        db_session.commit()

    # Delete
    def delete(self, id):
        group = db_session.query(MDMGroup).get(id)
        db_session.delete(group)

        db_session.commit()

    # [Deployment]
    class Deploy(Resource):
        # Redeploy
        def put(self, id):
            group = db_session.query(MDMGroup).get(id)
            devices = group.devices
            for device in devices:
                install_group_profiles_to_device(group, device)
            db_session.commit()

            for device in devices:
                push_to_device(device)
            return {'devices_count': len(devices)}

        # Undeploy
        def delete(self, id):
            group = db_session.query(MDMGroup).get(id)
            devices = group.devices
            for device in devices:
                remove_group_profiles_from_device(group, device)
            db_session.commit()

            for device in devices:
                push_to_device(device)
            return {'devices_count': len(devices)}


def create_api(debug=False):
    api_app = Blueprint('api_app', __name__)
    api = Api(api_app)
    api.debug = debug

    api.add_resource(ProfileResource, '/profiles', '/profile/<int:id>')
    api.add_resource(MDMGroupResource, '/mdm_groups', '/mdm_group/<int:id>', endpoint='mdmgroupresource')
    api.add_resource(MDMGroupResource.Deploy, '/mdm_group/<int:id>/deploy', endpoint='mdmgroupresource_deploy')

    return api_app
