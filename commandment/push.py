'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from OpenSSL import SSL
from OpenSSL.crypto import load_certificate, load_privatekey, FILETYPE_PEM
import sys, os, select, socket

import json
import struct

class NotificationPayload(object):
    def __init__(self, aps_dict):
        self.payload = {'aps': aps_dict}

    def as_json(self):
        return json.dumps(self.payload, separators=(',', ':')) # most compact JSON

class MDMNotificationPayload(NotificationPayload):
    def __init__(self, push_magic):
        self.payload = {'mdm': push_magic}

class Notification(object):
    def __init__(self):
        self.frame_items = []

    def append_frame_item(self, item):
        for i in self.frame_items:
            if i.item_id == item.item_id:
                raise Exception('already have frame item of type %d' % item.item_id)

        self.frame_items.append(item)

    def as_binary(self):
        frame_items = ''
        for i in self.frame_items:
            frame_items += i.as_binary()

        return struct.pack('!BI', 2, len(frame_items)) + frame_items

class FrameItem(object):
    def __init__(self, value):
        self.value = value

    def as_binary(self):
        pack_fmt = '!BH' + self.item_struct
        return struct.pack(pack_fmt, self.item_id, self.item_length, self.value)

class VariableLengthFrameItem(FrameItem):
    def as_binary(self):
        pack_fmt = '!BH%ss' % len(self.value)
        return struct.pack(pack_fmt, self.item_id, len(self.value), self.value)

class DeviceTokenFrame(FrameItem):
    item_id = 1
    item_length = 32
    item_struct = '32s'

class PayloadFrame(VariableLengthFrameItem):
    item_id = 2

    def __init__(self, notif_payload):
        self.notif_payload = notif_payload

    def as_binary(self):
        # generate value string on every call
        self.value = self.notif_payload.as_json()
        return super(PayloadFrame, self).as_binary()

class StrNotificationIdentifierFrame(FrameItem):
    item_id = 3
    item_length = 4
    item_struct = '4s'

class IntNotificationIdentifierFrame(StrNotificationIdentifierFrame):
    item_struct = 'I'

class ExpirationDateFrame(FrameItem):
    item_id = 4
    item_length = 4
    item_struct = 'I'

class PriorityFrame(FrameItem):
    item_id = 5
    item_length = 1
    item_struct = 'B'

def send_mdm_apns_notifications(apns_pkey, apns_cert, device_push_details):
    '''Deliver MDM APNS notifications to Apple APNS gateway

    Supports mutliple devices for efficient bulk notification. The parameter
    `device_push_details` should be a list of tuples that contain the
    (binary) Push Token and textual MDM Push Magic for each device desiring
    an MDM push notification.'''

    ssl_ctx = SSL.Context(SSL.SSLv23_METHOD)

    # re-wrap certificate & key into OpenSSL context from M2Crypto-abstractions
    cert = load_certificate(FILETYPE_PEM, apns_cert.get_pem().strip())
    ssl_ctx.use_certificate(cert)

    pkey = load_privatekey(FILETYPE_PEM, apns_pkey.get_pem().strip())
    ssl_ctx.use_privatekey(pkey)

    # development: gateway.sandbox.push.apple.com port 2195
    # production: gateway.push.apple.com port 2195

    sock = SSL.Connection(ssl_ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    sock.connect(('gateway.push.apple.com', 2195))

    for token, push_magic in device_push_details:
        notif = Notification()

        notif.append_frame_item(DeviceTokenFrame(token))
        notif.append_frame_item(PayloadFrame(MDMNotificationPayload(push_magic)))
        # notif.append_frame_item(StrNotificationIdentifierFrame('abcd'))
        notif.append_frame_item(ExpirationDateFrame(0)) # expires immediately
        # notif.append_frame_item(PriorityFrame(5)) # 10 = higher priority, but strictly defined for specific uses

        sock.send(notif.as_binary())

        # TODO: read status from socket?
        # TODO: perhaps read status from the feedback APNS service?

    sock.shutdown()
    sock.close()

