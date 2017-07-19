from flask import Blueprint, jsonify, g
from flask_rest_jsonapi import Api
import plistlib

from commandment.cms.decorators import verify_cms_signers
from .resources import DEPProfileList, DEPProfileDetail, DEPProfileRelationship

dep_app = Blueprint('dep_app', __name__)
api = Api(blueprint=dep_app)

api.route(DEPProfileList, 'dep_profile_list', '/v1/dep/profiles/')
api.route(DEPProfileDetail, 'dep_profile_detail', '/v1/dep/profiles/<int:dep_profile_id>')
api.route(DEPProfileRelationship, 'dep_profile_devices', '/v1/dep/profiles/<int:dep_profile_id>/relationships/devices')


@dep_app.route('/v1/dep/account', methods=["GET"])
def account():
    pass


@dep_app.route('/dep/profile', methods=["POST"])
@verify_cms_signers
def profile():
    """Accept a CMS Signed DER encoded XML data containing device information.

    This starts the DEP enrollment process.

    See Also:
        - **Request to a Profile URL** in the MDM Protocol Reference.
    """
    g.plist_data = plistlib.loads(g.signed_data)
