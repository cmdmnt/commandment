"""
This module contains API endpoints which do not fit with the JSON-API specification.
"""
import io
from flask import Blueprint, send_file, abort, current_app, jsonify
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.exc import NoResultFound
from .models import db, Certificate, RSAPrivateKey, Organization
from .schema import OrganizationFlatSchema

flat_api = Blueprint('flat_api', __name__)


@flat_api.route('/v1/organization', methods=['GET'])
def organization_get():
    """Retrieve information about the MDM home organization.

    Only returns a pseudo JSON-API representation because the standard has no definition for
    `singleton` resources.

    """
    try:
        o = db.session.query(Organization).one()
    except NoResultFound:
        return abort(400, 'No organization details found')
    
    org_schema = OrganizationFlatSchema()
    result = org_schema.dumps(o)

    return jsonify(result.data)


@flat_api.route('/v1/certificates/<int:certificate_id>/download')
def download_certificate(certificate_id: int):
    """Download a certificate in PEM format

    :reqheader Accept: application/x-pem-file
    :reqheader Accept: application/x-x509-user-cert
    :reqheader Accept: application/x-x509-ca-cert
    :resheader Content-Type: application/x-pem-file
    :resheader Content-Type: application/x-x509-user-cert
    :resheader Content-Type: application/x-x509-ca-cert
    :statuscode 200: OK
    :statuscode 404: There is no certificate configured
    :statuscode 400: Can't produce requested encoding
    """
    c = db.session.query(Certificate).filter(Certificate.id == certificate_id).one()
    bio = io.BytesIO(c.pem_data)

    return send_file(bio, 'application/x-pem-file', True, 'certificate.pem')


@flat_api.route('/v1/rsa_private_keys/<int:rsa_private_key_id>/download')
def download_key(rsa_private_key_id: int):
    """Download an RSA private key in PEM or DER format

    :reqheader Accept: application/x-pem-file
    :reqheader Accept: application/pkcs8
    :resheader Content-Type: application/x-pem-file
    :resheader Content-Type: application/pkcs8
    :statuscode 200: OK
    :statuscode 404: Not found
    :statuscode 400: Can't produce requested encoding
    """
    if not current_app.debug:
        abort(500, 'Not supported in this mode')

    c = db.session.query(RSAPrivateKey).filter(RSAPrivateKey.id == rsa_private_key_id).one()
    bio = io.BytesIO(c.pem_data)

    return send_file(bio, 'application/x-pem-file', True, 'rsa_private_key.pem')

