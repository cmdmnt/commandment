"""
This module contains a Blueprint for API endpoints relating to system configuration.
"""
from flask import Blueprint, abort, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from .models import db, Organization
from .schema import OrganizationFlatSchema, ProfileSchema

configuration_app = Blueprint('configuration_app', __name__)


@configuration_app.route('/organization', methods=['GET'])
def organization_get():
    """Retrieve information about the MDM home organization.

    :reqheader Accept: application/json
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :statuscode 200: Success
    :statuscode 404: No configuration available
    :statuscode 500: Other error
    """
    try:
        o = db.session.query(Organization).one()
    except NoResultFound:
        return abort(404, 'No organization details found')

    schema = OrganizationFlatSchema()
    dump = schema.dumps(o)

    return dump.data, 200, {'Content-Type': 'application/json'}


@configuration_app.route('/organization', methods=['PATCH', 'POST'])
def organization_post():
    """Update information about the MDM home organization.

    :reqheader Accept: application/json
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :statuscode 201: Success
    :statuscode 400: Validation Error
    :statuscode 500: Other error
    """
    schema = OrganizationFlatSchema()
    data = request.data
    result = schema.loads(data)
    db.session.commit()

    dump = schema.dumps(result.data)

    return dump.data, 200, {'Content-Type': 'application/json'}

