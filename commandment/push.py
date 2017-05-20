"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.

Attributes:
    apns_cxns (dict): A dictionary containing APNS connections keyed by the push certificate topic.
"""

import os
import apns2
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from oscrypto.keys import parse_pkcs12
from flask import g, current_app
from .models import Device
import json


def get_apns() -> apns2.APNSClient:
    apns = getattr(g, '_apns', None)

    if apns is None:
        push_certificate_path = current_app.config['PUSH_CERTIFICATE']
        if not os.path.exists(push_certificate_path):
            raise RuntimeError('You specified a push certificate at: {}, but it does not exist.'.format(push_certificate_path))

        # We can handle loading PKCS#12 but APNS2Client specifically requests PEM encoded certificates
        push_certificate_basename, ext = os.path.splitext(push_certificate_path)
        if ext.lower() == '.p12':
            pem_key_path = push_certificate_basename + '.key'
            pem_certificate_path = push_certificate_basename + '.crt'

            if not os.path.exists(pem_key_path) or not os.path.exists(pem_certificate_path):
                current_app.logger.info('You provided a PKCS#12 push certificate, we will have to encode it as PEM to continue...')
                current_app.logger.info('.key and .crt files will be saved in the same location')

                with open(push_certificate_path, 'rb') as fd:
                    if 'PUSH_CERTIFICATE_PASSWORD' in current_app.config:
                        key, certificate, intermediates = parse_pkcs12(fd.read(), bytes(current_app.config['PUSH_CERTIFICATE_PASSWORD'], 'utf8'))
                    else:
                        key, certificate, intermediates = parse_pkcs12(fd.read())

                crypto_key = serialization.load_der_private_key(key.dump(), None, default_backend())
                with open(pem_key_path, 'wb') as fd:
                    fd.write(crypto_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()))

                crypto_cert = x509.load_der_x509_certificate(certificate.dump(), default_backend())
                with open(pem_certificate_path, 'wb') as fd:
                    fd.write(crypto_cert.public_bytes(serialization.Encoding.PEM))

        try:
            apns = g._apns = apns2.APNSClient(mode='prod', client_cert=(pem_certificate_path, pem_key_path))
        except:
            raise RuntimeError('Your push certificate is expired or invalid')

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
    
    If the push token is invalid then it will be automatically set to None
    
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

    # 410 means that the token is no longer valid for this device, so don't attempt to push any more
    if response.status_code == 410:
        device.token = None
        device.push_magic = None

    return response
