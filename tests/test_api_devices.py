"""test_api_device.py: Tests for API device access"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import sys
import pytest
import json
import sqlalchemy
import sqlalchemy.orm
import uuid
from commandment import database as cdatabase
from commandment.models import Device, MDMGroup
from pytest_flask.fixtures import client
from flask import url_for

from fixtures import app

@pytest.fixture
def mdm_group():
    group_uuid = str(uuid.uuid4())

    group = {
        'group_name': 'Group test ' + group_uuid,
        'description': 'Test group',
    }

    return group

@pytest.fixture
def device():
    device_uuid = str(uuid.uuid4())

    device = {
        'udid': device_uuid,
        'serial_number': '90210',
        'groups': []
    }

    return device


class TestAPIDevice:
    @staticmethod
    def assert_success(response):
        if response.status_code != 200:
            raise AssertionError("Response status code is %d != 200" % response.status_code)
        return True

    @staticmethod
    def assert_json(headers):
        if 'Content-Type' not in headers:
            raise AssertionError("Response header did not have Content-Type")

        if headers['Content-Type'] != 'application/json':
            raise AssertionError("Response was not JSON")

        return True

    def test_put(self, client, device):
        res = client.put(url_for('api_app.deviceresource'), data=device)
        assert self.assert_json(res.headers)
        assert self.assert_success(res)

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

    def test_get(self, client, device):
        res = client.put(url_for('api_app.deviceresource'), data=device)
        data = json.loads(res.data)

        res = client.get(url_for('api_app.deviceresource', id=data['id']))

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

        device['id'] = data['id']
        assert device == data

    def test_delete(self, client, device):
        res = client.put(url_for('api_app.deviceresource'), data=device)
        data = json.loads(res.data)

        res = client.delete(url_for('api_app.deviceresource', id=data['id']))

        res = client.get(url_for('api_app.deviceresource', id=data['id']))

        assert res.status_code == 404

    def test_post(self, client, device):
        res = client.put(url_for('api_app.deviceresource'), data=device)
        data = json.loads(res.data)

        device['udid'] = str(uuid.uuid4())
        device['serial_number'] = '12131415'
        res = client.post(url_for('api_app.deviceresource', id=data['id']), data=device)

        assert self.assert_success(res)

        res = client.get(url_for('api_app.deviceresource', id=data['id']))

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        device['id'] = data['id']
        assert data == device
