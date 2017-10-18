from flask import Blueprint
from flask_rest_jsonapi import Api
from commandment.profiles.resources import ProfilesList, ProfileDetail, ProfileRelationship

profiles_api_app = Blueprint('profiles_api_app', __name__)
api = Api(blueprint=profiles_api_app)

# Profiles (Different to profiles returned by inventory)
api.route(ProfilesList, 'profiles_list', '/v1/profiles')
api.route(ProfileDetail, 'profile_detail', '/v1/profiles/<int:profile_id>')
api.route(ProfileRelationship, 'profile_tags', '/v1/profiles/<int:profile_id>/relationships/tags')
# api.route(PayloadsList, 'payloads_list', '/v1/payloads')
# api.route(PayloadDetail, 'payload_detail', '/v1/payloads/<int:payload_id>')
