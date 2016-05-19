'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from apns import APNs, Payload, Frame
import os
import tempfile
import atexit
from .database import db_session, NoResultFound
from .models import MDMConfig, Certificate as DBCertificate, Device, PrivateKey as DBPrivateKey, QueuedCommand
from .pki.ca import get_ca, PushCertificate
from .pki.m2certs import Certificate, RSAPrivateKey
import random
try:
    from ssl import SSLError
except ImportError:
    from socket import sslerror as SSLError

apns_cxns = {}

def push_init():
    q = db_session.query(DBCertificate, DBPrivateKey).join(DBCertificate, DBPrivateKey.certificates).filter(DBCertificate.cert_type == 'mdm.pushcert')

    for db_cert, db_pk in q:
        cert = PushCertificate.load(str(db_cert.pem_certificate))
        cert_topic = cert.get_topic()

        if cert_topic in apns_cxns:
            continue

        cert_handle, cert_file = tempfile.mkstemp()
        pkey_handle, pkey_file = tempfile.mkstemp()
        atexit.register(os.remove, pkey_file)
        atexit.register(os.remove, cert_file)
        os.write(cert_handle, db_cert.pem_certificate)
        os.write(pkey_handle, db_pk.pem_key)
        os.close(cert_handle)
        os.close(pkey_handle)

        apns = APNs(cert_file=cert_file, key_file=pkey_file, enhanced=True)
        apns_cxns[cert_topic] = apns

class MDMPayload(Payload):
    """A class representing an MDM APNs message payload"""
    def __init__(self, push_magic):
        self.mdm = push_magic

    def dict(self):
        return {'mdm': self.mdm}

def push_to_device(device_or_devices):
    # get an iterable list of devices even if one wasn't specified
    try:
        iter(device_or_devices)
    except TypeError:
        devices = (device_or_devices, )
    else:
        devices = device_or_devices

    # keyed access to topics for which we'll have an APNs connection for each
    topic_frames = {}

    for device in devices:

        if device.topic in apns_cxns:
            if device.topic not in topic_frames:
                # create our keyed topic reference if it doesn't exist
                topic_frames[device.topic] = Frame()

            # decode from as-stored base64 into hex encoding for apns library
            token_hex = device.token.decode('base64').encode('hex')

            mdm_payload = MDMPayload(device.push_magic)

            # add a frame for this topic
            topic_frames[device.topic].add_item(token_hex, mdm_payload, random.getrandbits(32), 0, 10)
        else:
            # TODO: configure and use real logging
            print 'Cannot send APNs to device: no APNs connection found (by device topic)'

    # loop through our by-topic APNs Frames and send away
    for topic in topic_frames.keys():
        try:
            apns_cxns[topic].gateway_server.send_notification_multiple(topic_frames[topic])
        except SSLError as e:
            msg = e.__str__()

            if 'sslv3 alert' in msg:
                # OpenSSL error telling us it received an SSL alert. We search
                # for a substring. See ssl/ssl_stat.c in OpenSSL sources for
                # lists of string output for SSL alerts. Full messages appear
                # like so:
                #
                # _ssl.c:504: error:14094416:SSL routines:SSL3_READ_BYTES:sslv3 alert certificate unknown

                if 'certificate unknown' in msg:
                    # Note: It seems an "unknown certificate" alert is thrown
                    # rather than an "expired" alert for MDM push certs that
                    # are, in fact, expired. Seems like an implimentation
                    # quirk that may change in the future.
                    raise Exception('MDM Push Certificate not accepted; possibly expired')

            raise
