from flask import Blueprint, jsonify, g, current_app, request, abort
from flask_rest_jsonapi import Api
from commandment.vpp.models import db, VPPAccount
from commandment.vpp.schema import VPPAccountSchema

vpp_app = Blueprint('vpp_app', __name__)
api = Api(blueprint=vpp_app)


@vpp_app.route('/api/v1/vpp/token', methods=['GET'])
def token():
    """Retrieve information about the current VPP token.

    :resheader Content-Type: application/json
    :statuscode 200:
    :statuscode 404: No VPP token has been uploaded
    """
    account = db.session.query(VPPAccount).first()
    schema = VPPAccountSchema()

    return schema.dumps(account)


@vpp_app.route('/api/v1/vpp/upload/token', methods=['POST'])
def upload_token():
    """Upload the VPP service token in the format normally issued by vpp.itunes.apple.com.

    :reqheader Accept: application/octet-stream
    :resheader Content-Type: application/json
    :statuscode 201: VPP token stored successfully.
    :statuscode 400: The request did not contain a valid VPP token.

    """
    if 'file' not in request.files:
        abort(400, 'no file uploaded in request data')

    f = request.files['file']

    if not f.content_type == 'application/octet-stream':
        abort(400, 'incorrect MIME type in request')

    data = f.read()
    account = VPPAccount(stoken=data)
    db.session.add(account)
    db.session.commit()

    return '{}', 201, {'Content-Type': 'application/json'}

