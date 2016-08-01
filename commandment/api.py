'''
Copyright (c) 2016 Flax & Teal Limited
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, current_app, abort
from flask.ext.restful import Api, Resource, reqparse
import json
from .models import Profile, MDMGroup, Device, ProfileStatus
from .profiles.service import ProfileService
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
parser.add_argument('description')
parser.add_argument('udid')
parser.add_argument('serial_number')


class DeviceResource(Resource):
    fillable = ('udid', 'serial_number')

    def __init__(self, *args, **kwargs):
        self.query = db_session.query(Device)
        super(DeviceResource, self).__init__(*args, **kwargs)

    # Create
    def put(self):
        args = parser.parse_args()

        device = Device(**{x: args[x] for x in self.fillable})
        db_session.add(device)

        if 'groups' in args and args['groups'] is not None:
            group_list = json.loads(args['groups']);
            device.mdm_groups = [db_session.query(MDMGroup).get(g['id']) for g in group_list]

        db_session.commit()

        return {'id': device.id}

    # Retrieve
    def get(self, id=None):
        if id:
            device = db_session.query(Device).get(id)

            if not device:
                return None, 404

            device_dict = device.as_dict()
            device_dict['groups'] = [g.as_dict() for g in device.mdm_groups]

            return device_dict

        query = db_session.query(Device)
        args = {k: v for k, v in parser.parse_args().items() if k in self.fillable and v is not None}

        if args:
            query = query.filter_by(**args)

        return [p.as_dict() for p in query.all()]

    # Update
    def post(self, id):
        args = parser.parse_args()

        device = db_session.query(Device).get(id)
        if not device:
            return None, 404

        device.update(**{x: args[x] for x in self.fillable if (x in args and args[x] is not None)})

        if 'groups' in args and args['groups'] is not None:
            group_list = json.loads(args['groups']);
            device.mdm_groups = [db_session.query(MDMGroup).get(g['id']) for g in group_list]

        db_session.commit()

    # Delete
    def delete(self, id):
        device = db_session.query(Device).get(id)
        db_session.delete(device)

        db_session.commit()

class ProfileResource(Resource):
    fillable = ('identifier', 'uuid', 'profile_data')

    def __init__(self, *args, **kwargs):
        self.query = db_session.query(Profile)
        super(ProfileResource, self).__init__(*args, **kwargs)

    # Create
    def put(self):
        args = parser.parse_args()

        profile = Profile(**{x: args[x] for x in self.fillable})
        db_session.add(profile)

        # You can't add groups en-mass here, as that requires a deployment
        # and status changes for each

        db_session.commit()

        return {'id': profile.id}

    # Retrieve
    def get(self, id=None):
        if id:
            profile = db_session.query(Profile).get(id)

            if not profile:
                return None, 404

            profile_dict = profile.as_dict()
            profile_dict['groups'] = [g.as_dict() for g in profile.mdm_groups]

            return profile_dict

        query = db_session.query(Profile)
        args = {k: v for k, v in parser.parse_args().items() if k in self.fillable and v is not None}

        if args:
            query = query.filter_by(**args)

        return [p.as_dict() for p in query.all()]

    # Update
    def post(self, id):
        args = parser.parse_args()

        profile = db_session.query(Profile).get(id)
        if not profile:
            return None, 404

        profile.update(**{x: args[x] for x in self.fillable if (x in args and args[x] is not None)})

        # Can't update groups for the reasons above

        db_session.commit()

    # Delete
    def delete(self, id):
        profile = db_session.query(Profile).get(id)

        if not profile:
            abort(404, "Profile not found")

        if profile.status == ProfileStatus.ACTIVE:
            profile_service = ProfileService()
            profile_service.remove(profile, delete=True)
        elif profile.status == ProfileStatus.INACTIVE:
            db_session.delete(profile)
        else:
            abort(400, "Can only delete a profile in a static (non-PENDING) state")

        db_session.commit()

    # [Deployment]
    class Deploy(Resource):
        # Redeploy
        def put(self, id):
            profile = db_session.query(Profile).get(id)

            profile_service = ProfileService()
            profile_service.install(profile)

            db_session.commit()

            return {"message": "Queued"}

        # Undeploy
        def delete(self, id):
            profile = db_session.query(Profile).get(id)

            profile_service = ProfileService()
            profile_service.remove(profile)

            db_session.commit()

            return {"message": "Queued"}

class MDMGroupResource(Resource):
    fillable = ('group_name', 'description')

    # Create
    def put(self):
        args = parser.parse_args()

        group = MDMGroup(**{x: args[x] for x in self.fillable})
        db_session.add(group)

        db_session.commit()

        return {'id': group.id}

    # Retrieve
    def get(self, id=None):
        if id:
            mdm_group = db_session.query(MDMGroup).get(id)

            if not mdm_group:
                return None, 404

            return mdm_group.as_dict()

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

    # [Profiles]
    class Profile(Resource):
        def put(self, id, profile_id):
            group = db_session.query(MDMGroup).get(id)
            profile = db_session.query(Profile).get(profile_id)

            if profile in group.profiles:
                return {"message": "Already in group"}

            if profile.status != ProfileStatus.INACTIVE:
                return abort(400, "Cannot change groups while profile is not inactive")

            group.profiles.append(profile)
            db_session.commit()

            return {"message": "Success"}

        def delete(self, id, profile_id):
            group = db_session.query(MDMGroup).get(id)
            profile = db_session.query(Profile).get(profile_id)

            if profile not in group.profiles:
                return abort(400, "Not in group")

            if profile.status != ProfileStatus.INACTIVE:
                return abort(400, "Cannot change groups while profile is not inactive")

            group.profiles.remove(profile)
            db_session.commit()

            return {"message": "Success"}

    # [Devices]
    class Device(Resource):
        def put(self, id, device_id):
            current_app.logger.info('Added device to group')
            group = db_session.query(MDMGroup).get(id)
            device = db_session.query(Device).get(device_id)
            profile_service = ProfileService()

            if device in group.devices:
                return {"message": "Already in group"}

            for profile in group.profiles:
                if profile.status == ProfileStatus.ACTIVE:
                    profile_service.finalize_installation(profile, device)

            db_session.commit()

            group.devices.append(device)

            db_session.commit()

            return {"message": "Success"}

        def delete(self, id, device_id):
            group = db_session.query(MDMGroup).get(id)
            device = db_session.query(Device).get(device_id)
            profile_service = ProfileService()

            if device not in group.devices:
                return abort(400, str(group.devices))

            currently_deployed_profiles = [profile for profile in group.profiles if profile.status == ProfileStatus.ACTIVE]
            group.devices.remove(device)

            # We do not want group changes in a separate job to affect this device while we remove profiles
            db_session.commit()

            # Event (and job) would be better here (an ORM event would possibly not give us the correct sequence of calls)
            # FIXME: what happens if a profile is pending removal before this but job enacted afterwards?
            for profile in group.profiles:
                if profile.status == ProfileStatus.ACTIVE:
                    profile_service.finalize_removal(profile, device)

            db_session.commit()

            return {"message": "Success"}


def create_api(debug=False):
    api_app = Blueprint('api_app', __name__)
    api = Api(api_app)
    api.debug = debug

    api.add_resource(ProfileResource, '/profiles', '/profile/<int:id>')
    api.add_resource(ProfileResource.Deploy, '/profile/<int:id>/deploy', endpoint='profileresource_deploy')
    api.add_resource(DeviceResource, '/devices', '/device/<int:id>')
    api.add_resource(MDMGroupResource, '/mdm_groups', '/mdm_group/<int:id>', endpoint='mdmgroupresource')
    api.add_resource(MDMGroupResource.Profile, '/mdm_group/<int:id>/profile/<int:profile_id>', endpoint='mdmgroupresource_profile')
    api.add_resource(MDMGroupResource.Device, '/mdm_group/<int:id>/device/<int:device_id>', endpoint='mdmgroupresource_device')

    return api_app
