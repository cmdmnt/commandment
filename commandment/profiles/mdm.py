"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from typing import Set
from . import Payload, DeviceAttributes
from ..mdm import AccessRights


class MDMPayload(Payload):
    payload_type = 'com.apple.mdm'

    def __init__(self, identifier, identity_cert_uuid, topic, server_url, access_rights=AccessRights.All, **kwargs):
        super(MDMPayload, self).__init__(self.payload_type, identifier, **kwargs)

        # mandatory MDM payload fields
        self.payload['IdentityCertificateUUID'] = identity_cert_uuid
        self.payload['Topic'] = topic
        self.payload['ServerURL'] = server_url
        self.payload['AccessRights'] = access_rights.value

        # optional MDM payload fields. specify in kwargs if desired
        #   ServerCapabilities (MDM extensions; mandatory for OS X management)
        #   SignMessage
        #   CheckInURL
        #   CheckOutWhenRemoved [iOS 5+, OS X 10.9+, unconditional on OS X 10.8]
        #   UseDevelopmentAPNS


class ProfileServicePayload(Payload):
    payload_type = 'Profile Service'

    def __init__(self, identifier: str, device_attributes: Set[DeviceAttributes], challenge: str = None, **kwargs):
        super(ProfileServicePayload, self).__init__(self.payload_type, identifier, **kwargs)

        self.payload['URL'] = 'https://commandment.dev:5443/ota/profile'
        self.payload['DeviceAttributes'] = device_attributes

        if challenge is not None:
            self.payload['Challenge'] = challenge

