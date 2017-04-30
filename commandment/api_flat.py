"""
This module contains API endpoints which do not fit with the JSON-API specification.
"""
import io
from flask import Blueprint, send_file, abort, current_app, jsonify, request, make_response
from sqlalchemy.orm.exc import NoResultFound
import plistlib
from .models import db, Certificate, RSAPrivateKey, Organization, Device, Command, InstalledCertificate
from .profiles.models import Profile
from .mdm import commands
from .schema import OrganizationFlatSchema, ProfileSchema
from .profiles.schema import ProfileSchema as ProfilePlistSchema

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


@flat_api.route('/v1/download/certificates/<int:certificate_id>')
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


@flat_api.route('/v1/installed_certificates/<int:installed_certificate_id>/download')
def download_installed_certificate(installed_certificate_id: int):
    """Download an installed X.509 certificate as DER encoded

    :reqheader Accept: application/x-x509-ca-cert
    :resheader Content-Type: application/x-x509-ca-cert
    :statuscode 200: OK
    :statuscode 404: Not found
    :statuscode 400: Can't produce requested encoding
    """
    c = db.session.query(InstalledCertificate).filter(InstalledCertificate.id == installed_certificate_id).one()
    bio = io.BytesIO(c.der_data)

    return send_file(bio, 'application/x-x509-ca-cert', True, 'certificate.crt')


@flat_api.route('/v1/devices/inventory/<int:device_id>')
def device_inventory(device_id: int):
    """Tell a device to produce a full inventory immediately.
    
    This is mostly for testing right now.
    
    :statuscode 200: OK
    """
    d = db.session.query(Device).filter(Device.id == device_id).one()

    # DeviceInformation
    di = commands.DeviceInformation.for_platform(d.platform, d.os_version)
    db_command = Command.from_model(di)
    db_command.device = d
    db.session.add(db_command)

    # InstalledApplicationList
    # ial = commands.InstalledApplicationList()
    # db_command_ial = Command.from_model(ial)
    # db_command_ial.device = d
    # db.session.add(db_command_ial)

    # CertificateList
    cl = commands.CertificateList()
    dbc = Command.from_model(cl)
    dbc.device = d
    db.session.add(dbc)

    # SecurityInfo
    si = commands.SecurityInfo()
    dbsi = Command.from_model(si)
    dbsi.device = d
    db.session.add(dbsi)

    # ProfileList
    pl = commands.ProfileList()
    db_pl = Command.from_model(pl)
    db_pl.device = d
    db.session.add(db_pl)

    db.session.commit()

    return 'OK'


@flat_api.route('/v1/upload/profiles', methods=['POST'])
def upload_profile():
    """Upload a custom profile using multipart/form-data I.E from an upload input.

    Encrypted profiles are not supported.

    The profiles contents will be stored using the following process:
    - For the top level profile (and each payload) there is a marshmallow schema which maps the payload keys into
        the SQLAlchemy model keys. It is also the responsibility of the marshmallow schema to be the validator for 
        uploaded profiles.
    - The profile itself is inserted as a Profile model.
    - Each payload is unmarshalled using marshmallow to a specific Payload model. Each specific model contains a join
        table inheritance to the base ``payloads`` table.

    The returned body contains a jsonapi object with details of the newly created profile and associated payload ID's.

    Note: Does not support ``application/x-www-form-urlencoded``

    TODO:
        - Support signed profiles

    :reqheader Accept: application/vnd.api+json
    :reqheader Content-Type: multipart/form-data
    :resheader Content-Type: application/vnd.api+json
    :statuscode 201: profile created
    :statuscode 400: If the request contained malformed or missing payload data.
    :statuscode 500: If something else went wrong with parsing or persisting the payload(s)
    """
    if 'file' not in request.files:
        abort(400, 'no file uploaded in request data')

    f = request.files['file']

    if not f.content_type == 'application/x-apple-aspen-config':
        abort(400, 'incorrect MIME type in request')

    try:
        data = f.read()
        plist = plistlib.loads(data)

        profile = ProfilePlistSchema().load(plist).data
    except plistlib.InvalidFileException as e:
        current_app.logger.error(e)
        abort(400, 'invalid plist format supplied')

    except BaseException as e:  # TODO: separate errors for exceptions caught here
        current_app.logger.error(e)
        abort(400, 'cannot parse the supplied profile')

    db.session.add(profile)
    db.session.commit()

    profile_schema = ProfileSchema()
    model_data = profile_schema.dump(profile).data
    resp = make_response(jsonify(model_data), 201, {'Content-Type': 'application/vnd.api+json'})
    return resp


@flat_api.route('/v1/download/profiles/<int:profile_id>')
def download_profile(profile_id: int):
    """Download a profile.
    
    The profile is reconstructed from its database representation.
    
    Args:
        profile_id (int): The profile id 

    :reqheader Accept: application/x-apple-aspen-config
    :resheader Content-Type: application/x-apple-aspen-config
    :statuscode 200:
    :statuscode 404:
    :statuscode 500:
    """
    try:
        profile = db.session.query(Profile).filter(Profile.id == profile_id).one()
    except NoResultFound:
        abort(404)

    schema = ProfilePlistSchema()
    result = schema.dump(profile)

    return plistlib.dumps(result.data, skipkeys=True), 200, {'Content-Type': 'application/x-apple-aspen-config'}

