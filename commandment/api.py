"""
    This module contains all of the API generated using the Flask-REST-JSONAPI extension.
"""
from flask import Blueprint
from flask_rest_jsonapi import Api
from .resources import CertificatesList, CertificateDetail, CertificateSigningRequestList, \
    CertificateSigningRequestDetail, PushCertificateList, SSLCertificatesList, \
    CACertificateList, PrivateKeyDetail, DeviceList, DeviceDetail, OrganizationList, \
    OrganizationDetail, CommandsList, CommandDetail, InstalledApplicationsList, ProfilesList, ProfileDetail, \
    InstalledCertificatesList, InstalledCertificateDetail, InstalledApplicationDetail, \
    DeviceGroupList, DeviceGroupDetail, DeviceRelationship, CommandRelationship, InstalledProfilesList, \
    InstalledProfileDetail, TagsList, TagDetail, TagRelationship, ProfileRelationship

# PayloadsList, PayloadDetail,

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
api.route(DeviceList, 'devices_list', '/v1/devices', '/v1/device_groups/<int:device_group_id>/devices')
api.route(DeviceDetail, 'device_detail', '/v1/devices/<int:device_id>')
api.route(DeviceRelationship, 'device_commands', '/v1/devices/<int:device_id>/relationships/commands')
api.route(DeviceRelationship, 'device_tags', '/v1/devices/<int:id>/relationships/tags')

api.route(DeviceGroupList, 'device_groups_list', '/v1/device_groups', '/v1/devices/<int:device_id>/groups')
api.route(DeviceGroupDetail, 'device_group_detail', '/v1/device_groups/<int:device_group_id>')
api.route(DeviceRelationship, 'device_group_devices', '/v1/device_groups/<int:device_group_id>/relationship/devices')

# Commands
api.route(CommandsList, 'commands_list', '/v1/commands', '/v1/devices/<int:device_id>/commands')
api.route(CommandDetail, 'command_detail', '/v1/commands/<int:command_id>')

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

# Profiles (Different to profiles returned by inventory)
api.route(ProfilesList, 'profiles_list', '/v1/profiles')
api.route(ProfileDetail, 'profile_detail', '/v1/profiles/<int:profile_id>')
api.route(ProfileRelationship, 'profile_tags', '/v1/profiles/<int:profile_id>/relationships/tags')
# api.route(PayloadsList, 'payloads_list', '/v1/payloads')
# api.route(PayloadDetail, 'payload_detail', '/v1/payloads/<int:payload_id>')

api.route(InstalledProfilesList, 'installed_profiles_list', '/v1/installed_profiles',
          '/v1/devices/<int:device_id>/installed_profiles')
api.route(InstalledProfileDetail, 'installed_profile_detail', '/v1/installed_profiles/<int:installed_profile_id>')


# Organizations
# api.route(OrganizationList, 'organizations_list', '/v1/organizations')
# api.route(OrganizationDetail, 'organization_detail', '/v1/organizations/<int:organization_id>')


api.route(TagsList, 'tags_list', '/v1/tags')
api.route(TagDetail, 'tag_detail', '/v1/tags/<tag_id>')
api.route(TagRelationship, 'tag_devices', '/v1/tags/<tag_id>/relationships/devices')

