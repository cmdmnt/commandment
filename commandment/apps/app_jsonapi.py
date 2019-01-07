from flask import Blueprint, request
from flask_rest_jsonapi import Api

from commandment.apps.resources import ApplicationDetail, ApplicationList
from commandment.api.resources import DeviceRelationship

api_app = Blueprint('applications_api', __name__)
api = Api(blueprint=api_app)

api.route(ApplicationList, 'applications_list',
          '/v1/applications')
api.route(ApplicationDetail, 'application_detail',
          '/v1/applications/<int:application_id>')
#api.route(DeviceRelationship, 'application_devices',
#          '/v1/applications/<int:application_id>/relationship/devices')
