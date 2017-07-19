from cryptography.hazmat.backends import default_backend
from flask import Blueprint, jsonify, g, current_app
from flask_rest_jsonapi import Api
import plistlib
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding
from base64 import urlsafe_b64encode

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


@dep_app.route('/dep/anchor_certs', methods=["GET"])
def anchor_certs():
    """Download a list of certificates to trust the MDM

    The response is a JSON array of base64 encoded DER certs as described in the DEP profile creation documentation."""
    anchors = []

    if 'CA_CERTIFICATE' in current_app.config:
        with open(current_app.config['CA_CERTIFICATE'], 'rb') as fd:
            pem_data = fd.read()
            c: x509.Certificate = x509.load_pem_x509_certificate(pem_data, backend=default_backend())
            der = c.public_bytes(Encoding.DER)
            anchors.append(urlsafe_b64encode(der))

    if 'SSL_CERTIFICATE' in current_app.config:
        with open(current_app.config['SSL_CERTIFICATE'], 'rb') as fd:
            pem_data = fd.read()
            c: x509.Certificate = x509.load_pem_x509_certificate(pem_data, backend=default_backend())
            der = c.public_bytes(Encoding.DER)
            anchors.append(urlsafe_b64encode(der))

    return jsonify(anchors)
