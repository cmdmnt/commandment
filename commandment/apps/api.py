from flask import Blueprint
from commandment.apps.resources import ApplicationDetail, ApplicationList
from commandment.api.resources import DeviceRelationship
from commandment.api.app_jsonapi import api

api_app = Blueprint('applications_api', __name__)

api.route(ApplicationList, 'applications_list',
          '/v1/applications')
api.route(ApplicationDetail, 'application_detail',
          '/v1/applications/<int:application_id>')
#api.route(DeviceRelationship, 'application_devices',
#          '/v1/applications/<int:application_id>/relationship/devices')
