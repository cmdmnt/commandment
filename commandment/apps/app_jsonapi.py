from flask import Blueprint, request
from flask_rest_jsonapi import Api

from commandment.apps.resources import ApplicationDetail, ApplicationList, ApplicationRelationship


api_app = Blueprint('applications_api', __name__)
api = Api(blueprint=api_app)

api.route(ApplicationList, 'applications_list',
          '/v1/applications')
api.route(ApplicationDetail, 'application_detail',
          '/v1/applications/<int:application_id>')
api.route(ApplicationRelationship, 'application_tags', '/v1/applications/<int:application_id>/relationships/tags')
