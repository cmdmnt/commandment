"""test_api_group_deploy.py: Tests for group deployment API."""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import sys
import pytest
import json
import sqlalchemy
import sqlalchemy.orm
import uuid
from commandment import database as cdatabase
from commandment.models import Profile, MDMGroup
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
def profile():
    profile_uuid = str(uuid.uuid4())

    profile = {
        'identifier': 'com.example.test.' + profile_uuid,
        'uuid': profile_uuid,
        'profile_data': ''
    }

    return profile


class TestAPIProfile:
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

    def test_redeploy(self, client, profile, mdm_group):
        profile = Profile(**profile)
        mdm_group = MDMGroup(**mdm_group)

        cdatabase.db_session.add(profile)
        cdatabase.db_session.add(mdm_group)
        profile.mdm_groups.append(mdm_group)
        cdatabase.db_session.commit()

        res = client.put(url_for('api_app.mdmgroupresource_deploy', id=mdm_group.id))

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        assert 'devices_count' in data
        assert data['devices_count'] == 0

    def test_undeploy(self, client, profile, mdm_group):
        profile = Profile(**profile)
        mdm_group = MDMGroup(**mdm_group)

        cdatabase.db_session.add(profile)
        cdatabase.db_session.add(mdm_group)
        profile.mdm_groups.append(mdm_group)
        cdatabase.db_session.commit()

        res = client.delete(url_for('api_app.mdmgroupresource_deploy', id=mdm_group.id))

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        assert 'devices_count' in data
        assert data['devices_count'] == 0
