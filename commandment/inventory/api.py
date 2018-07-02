from flask import Blueprint, send_file
from flask_rest_jsonapi import Api
import io

from commandment.inventory.models import db, InstalledCertificate
from commandment.inventory.resources import InstalledApplicationsList, InstalledApplicationDetail, \
    InstalledCertificatesList, InstalledCertificateDetail, InstalledProfilesList, InstalledProfileDetail, \
    AvailableOSUpdateList, AvailableOSUpdateDetail
from commandment.api.app_jsonapi import api

api_app = Blueprint('inventory_api_app', __name__)
# api = Api(blueprint=api_app)

# InstalledApplications
api.route(InstalledApplicationsList, 'installed_applications_list',
          '/v1/installed_applications', '/v1/devices/<int:device_id>/installed_applications')
api.route(InstalledApplicationDetail, 'installed_application_detail',
          '/v1/installed_applications/<int:installed_application_id>')

# InstalledCertificates
api.route(InstalledCertificatesList, 'installed_certificates_list',
          '/v1/installed_certificates', '/v1/devices/<int:device_id>/installed_certificates')
api.route(InstalledCertificateDetail, 'installed_certificate_detail',
          '/v1/installed_certificates/<int:installed_certificate_id>')

api.route(InstalledProfilesList, 'installed_profiles_list', '/v1/installed_profiles',
          '/v1/devices/<int:device_id>/installed_profiles')
api.route(InstalledProfileDetail, 'installed_profile_detail', '/v1/installed_profiles/<int:installed_profile_id>')



# Available OS Updates
api.route(AvailableOSUpdateList, 'available_os_updates_list',
          '/v1/available_os_updates', '/v1/devices/<int:device_id>/available_os_updates')
api.route(AvailableOSUpdateDetail, 'available_os_update_detail',
          '/v1/available_os_updates/<int:available_os_update_id>')


@api_app.route('/v1/installed_certificates/<int:installed_certificate_id>/download')
def download_installed_certificate(installed_certificate_id: int):
    """Download an installed certificate asx a DER encoded X.509 certificate.

    The file name will be a stripped version of the X.509 Common Name, with a .crt extension.

    :reqheader Accept: application/x-x509-ca-cert
    :resheader Content-Type: application/x-x509-ca-cert
    :statuscode 200: OK
    :statuscode 404: Not found
    :statuscode 400: Can't produce requested encoding
    """
    c = db.session.query(InstalledCertificate).filter(InstalledCertificate.id == installed_certificate_id).one()
    bio = io.BytesIO(c.der_data)

    prefix = c.x509_cn.strip('/\:') if c.x509_cn is not None else 'certificate'

    return send_file(bio, 'application/x-x509-ca-cert', True, '{}.crt'.format(prefix))
