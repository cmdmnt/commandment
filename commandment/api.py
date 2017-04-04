import io
from flask import Blueprint, send_file, current_app, abort, jsonify
from flask_rest_jsonapi import Api
from .resources import CertificatesList, CertificateDetail, CertificateSigningRequestList, \
    CertificateSigningRequestDetail, PushCertificateList, SSLCertificatesList, \
    CACertificateList, PrivateKeyDetail, DeviceList, DeviceDetail, OrganizationList, \
    OrganizationDetail, CommandsList, CommandDetail

api_app = Blueprint('api_app', __name__)
api = Api(api_app)

# Certificates
api.route(CertificatesList, 'certificates_list', '/v1/certificates/')
api.route(CertificateDetail, 'certificate_detail', '/v1/certificates/<int:certificate_id>')

api.route(CertificateSigningRequestList, 'certificate_signing_request_list', '/v1/certificate_signing_requests')
api.route(CertificateSigningRequestDetail, 'certificate_signing_request_detail',
          '/v1/certificate_signing_requests/<int:certificate_signing_request_id>')
api.route(PushCertificateList, 'push_certificates_list', '/v1/push_certificates/')
api.route(SSLCertificatesList, 'ssl_certificates_list', '/v1/ssl_certificates/')
api.route(CACertificateList, 'ca_certificates_list', '/v1/ca_certificates/')
api.route(PrivateKeyDetail, 'private_key_detail', '/v1/rsa_private_keys/<int:private_key_id>')


# Devices
api.route(DeviceList, 'devices_list', '/v1/devices')
api.route(DeviceDetail, 'device_detail', '/v1/devices/<int:id>')

# Commands
api.route(CommandsList, 'commands_list', '/v1/commands', '/v1/devices/<int:device_id>/commands')
api.route(CommandDetail, 'command_detail', '/v1/commands/<int:command_id>')

# Organizations
# api.route(OrganizationList, 'organizations_list', '/v1/organizations')
# api.route(OrganizationDetail, 'organization_detail', '/v1/organizations/<int:organization_id>')

