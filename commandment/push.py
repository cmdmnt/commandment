"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.

Attributes:
    apns_cxns (dict): A dictionary containing APNS connections keyed by the push certificate topic.
"""

import os
import apns2
from flask import g, current_app
from .models import Device
import json


def get_apns() -> apns2.APNSClient:
    apns = getattr(g, '_apns', None)
    if apns is None:
        pushcert_path = current_app.config['PUSH_CERTIFICATE']
        if not os.path.exists(pushcert_path):
            raise RuntimeError('You specified a push certificate at: {}, but it does not exist.'.format(pushcert_path))
        
        apns = g._apns = apns2.APNSClient(mode='prod', client_cert=pushcert_path)
    return apns


class MDMPayload(apns2.Payload):
    """A class representing an MDM APNs message payload."""
    def __init__(self, push_magic: str):
        """Constructor
        
            Args:
                push_magic (str): The push magic token that was supplied by an enrolled device.
        """
        super(MDMPayload, self).__init__(custom={'mdm': push_magic})
        self._push_magic = push_magic

    def to_json(self) -> bytes:
        return json.dumps({'mdm': self._push_magic})


def push_to_device(device: Device) -> apns2.Response:
    """Issue a `Blank Push` to a device.
    
    Args:
        device (Device): The device model to push to, must have a valid apns token and push magic
          
    Returns:
        APNS2Client Response object
    """
    current_app.logger.debug('Sending a push notification to {} on topic {}, using push magic: {}'.format(
        device.hex_token, device.topic, device.push_magic
    ))
    client = get_apns()
    payload = MDMPayload(device.push_magic)
    notification = apns2.Notification(payload, priority=apns2.PRIORITY_LOW)
    response = client.push(notification, device.hex_token, device.topic)

    # TODO: Status 410 means the device token doesnt exist anymore

    return response
