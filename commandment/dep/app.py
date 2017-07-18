from flask import Blueprint, jsonify
from flask_rest_jsonapi import Api
from .resources import DEPProfileList, DEPProfileDetail, DEPProfileRelationship

dep_app = Blueprint('dep_app', __name__)
api = Api(blueprint=dep_app)

api.route(DEPProfileList, 'dep_profile_list', '/v1/dep/profiles/')
api.route(DEPProfileDetail, 'dep_profile_detail', '/v1/dep/profiles/<int:dep_profile_id>')
api.route(DEPProfileRelationship, 'dep_profile_devices', '/v1/dep/profiles/<int:dep_profile_id>/relationships/devices')


@dep_app.route('/v1/dep/account', methods=["GET"])
def account():
    pass
