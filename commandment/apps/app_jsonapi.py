from flask import Blueprint, request
from flask_rest_jsonapi import Api

from commandment.apps.resources import ApplicationDetail, ApplicationList, ApplicationRelationship, \
    ManagedApplicationList, ManagedApplicationDetail, ManagedApplicationRelationship, MASApplicationList, \
    MASApplicationDetail, IOSApplicationList, IOSApplicationDetail

api_app = Blueprint('applications_api', __name__)
api = Api(blueprint=api_app)

api.route(ApplicationList, 'applications_list',
          '/v1/applications')
api.route(ApplicationDetail, 'application_detail',
          '/v1/applications/<int:application_id>')
api.route(ApplicationRelationship, 'application_tags', '/v1/applications/<int:application_id>/relationships/tags')
api.route(ManagedApplicationList, 'managed_applications_list',
          '/v1/managed_applications')
api.route(ManagedApplicationDetail, 'managed_application_detail',
          '/v1/managed_applications/<int:managed_application_id>')
api.route(ManagedApplicationRelationship, 'managed_application_device',
          '/v1/managed_applications/<int:application_id>/relationships/device')

# Platform specific subclasses

api.route(MASApplicationList, 'mas_applications_list',
          '/v1/applications/store/mac')
api.route(MASApplicationDetail, 'mas_application_detail',
          '/v1/applications/store/mac/<int:application_id>')

api.route(IOSApplicationList, 'ios_applications_list',
          '/v1/applications/store/ios')
api.route(IOSApplicationDetail, 'ios_application_detail',
          '/v1/applications/store/ios/<int:application_id>')


