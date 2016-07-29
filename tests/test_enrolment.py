"""test_enrolment.py: Tests for enrolment behaviour"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

from commandment import database as cdatabase
from commandment.mdm import enroll
from commandment.models import Device
import json

from fixtures import app


class TestEnrolment:
    def test_enroll_from_plist_finds_existing_device(self, app):
        plist = {
            'UDID': '9b99e22c-c6b3-4768-8ab5-76c29f4021ac',
            'SERIAL': '7b2c5e8e-4457-4a34-a942-05d5973c619e'
        }
        device = Device()
        device.serial_number = plist['SERIAL']
        device.udid = plist['UDID']
        cdatabase.db_session.add(device)
        cdatabase.db_session.commit()

        redis_client = app.redis_store._redis_client

        pubsub = {}
        for channel in ('enroll', 'serial'):
            pubsub_channel = redis_client.pubsub()
            pubsub_channel.subscribe('commandment.' + channel)
            pubsub_channel.get_message()
            pubsub[channel] = pubsub_channel

        new_device = enroll.enroll_from_plist(plist)

        message = pubsub['enroll'].get_message()['data']
        assert pubsub['enroll'].get_message() is None

        payload = json.loads(message)
        assert payload == {'udid': plist['UDID']}

        message = pubsub['serial'].get_message()['data']
        assert pubsub['serial'].get_message() is None

        payload = json.loads(message)
        assert payload == {'udid': plist['UDID'], 'serial_number': plist['SERIAL']}
        assert new_device.id == device.id
