'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from . import Payload

# MDM Access Rights (AR)
MDM_AR__ALLOW_INSPECT_CONFIG_PROF = 1
MDM_AR__ALLOW_INST_REM_CONFIG_PROF = 2
MDM_AR__ALLOW_DEVICE_LOCK = 4
MDM_AR__ALLOW_DEVICE_ERASE = 8
MDM_AR__ALLOW_DEVICE_QUERY = 16
MDM_AR__ALLOW_NETWORK_QUERY = 32
MDM_AR__ALLOW_INSPECT_PROV_PROF = 64
MDM_AR__ALLOW_INST_REM_PROV_PROF = 128
MDM_AR__ALLOW_INSPECT_APPS = 256
MDM_AR__ALLOW_RESTRICTION_QUERY = 512
MDM_AR__ALLOW_SECURITY_QUERY = 1024
MDM_AR__ALLOW_SETTINGS_MANIP = 2048
MDM_AR__ALLOW_APP_MGMT = 4096

MDM_AR__ALL = \
            MDM_AR__ALLOW_INSPECT_CONFIG_PROF | \
            MDM_AR__ALLOW_INST_REM_CONFIG_PROF | \
            MDM_AR__ALLOW_DEVICE_LOCK | \
            MDM_AR__ALLOW_DEVICE_ERASE | \
            MDM_AR__ALLOW_DEVICE_QUERY | \
            MDM_AR__ALLOW_NETWORK_QUERY | \
            MDM_AR__ALLOW_INSPECT_PROV_PROF | \
            MDM_AR__ALLOW_INST_REM_PROV_PROF | \
            MDM_AR__ALLOW_INSPECT_APPS | \
            MDM_AR__ALLOW_RESTRICTION_QUERY | \
            MDM_AR__ALLOW_SECURITY_QUERY | \
            MDM_AR__ALLOW_SETTINGS_MANIP | \
            MDM_AR__ALLOW_APP_MGMT

class MDMPayload(Payload):
    payload_type = 'com.apple.mdm'

    def __init__(self, identifier, identity_cert_uuid, topic, server_url, access_rights=MDM_AR__ALL, **kwargs):
        super(MDMPayload, self).__init__(self.payload_type, identifier, **kwargs)

        # mandatory MDM payload fields
        self.payload['IdentityCertificateUUID'] = identity_cert_uuid
        self.payload['Topic'] = topic
        self.payload['ServerURL'] = server_url
        self.payload['AccessRights'] = access_rights

        # optional MDM payload fields. specify in kwargs if desired
        #   ServerCapabilities (MDM extensions; mandatory for OS X management)
        #   SignMessage
        #   CheckInURL
        #   CheckOutWhenRemoved [iOS 5+, OS X 10.9+, unconditional on OS X 10.8]
        #   UseDevelopmentAPNS
