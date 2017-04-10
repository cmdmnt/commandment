"""
This module implements the profile delivery service as described in "Over-The-Air profile delivery".
This is the preferred mechanism for non-DEP enrolment.

The welcome page should be available at /ota/
"""
from flask import Blueprint, send_file, abort, current_app, jsonify

ota_app = Blueprint('ota_app', __name__)


@ota_app.route('/')
def welcome():
    """This page should be used as the landing site for OAuth2 authentication. A token should be generated which will
    then be passed as the challenge in the ``Profile Service`` payload."""
    pass

