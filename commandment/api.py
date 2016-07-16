'''
Copyright (c) 2016 Flax & Teal Limited
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint
from flask.ext.restful import Api, Resource, reqparse
from .models import Profile
from .database import db_session


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('identifier')
parser.add_argument('uuid')
parser.add_argument('profile_data')


class ProfileResource(Resource):
    fillable = ('identifier', 'uuid', 'profile_data')

    def __init__(self, *args, **kwargs):
        self.query = db_session.query(Profile)
        super(ProfileResource, self).__init__(*args, **kwargs)

    # Create
    def put(self):
        args = parser.parse_args()

        profile = Profile(*[args[x] for x in self.fillable])
        db_session.add(profile)
        db_session.commit()

        return {'id': profile.id}

    # Retrieve
    def get(self, id):
        profile = db_session.query(Profile).get(id)

        return profile.as_dict() if profile else (None, 404)

    # Update
    def post(self, id):
        args = parser.parse_args()

        profile = db_session.query(Profile).get(id)
        profile.update(**{x: args[x] for x in self.fillable if x in args})

        db_session.commit()

    # Delete
    def delete(self, id):
        profile = db_session.query(Profile).get(id)
        db_session.delete(profile)

        db_session.commit()


def create_api(debug=False):
    api_app = Blueprint('api_app', __name__)
    api = Api(api_app)
    api.debug = debug

    api.add_resource(ProfileResource, '/profiles', '/profiles/<int:id>')

    return api_app
