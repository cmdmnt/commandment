"""test_api_profile.py: Tests for API profile access"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import sys
import pytest
import json
import sqlalchemy
import sqlalchemy.orm
import uuid
from commandment import app as capp, database as cdatabase
from commandment.models import Profile, MDMGroup
from pytest_flask.fixtures import client
from flask import url_for

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
        'profile_data': '',
        'groups': []
    }

    return profile

@pytest.yield_fixture(scope="session")
def app():
    app = capp.create_app(debug=True)
    cdatabase.config_engine('sqlite://', echo=True)
    #sessionmaker = sqlalchemy.orm.sessionmaker(
    #    autocommit=False,
    #    autoflush=False,
    #    bind=engine
    #)
    #session = sqlalchemy.orm.scoped_session(sessionmaker)
    cdatabase.init_db()
    connection = cdatabase.engine.connect()

    yield app

    connection.close()
    cdatabase.Base.metadata.drop_all(bind=cdatabase.engine)


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

    def test_put(self, client, profile):
        res = client.put(url_for('api_app.profileresource'), data=profile)
        assert self.assert_json(res.headers)
        assert self.assert_success(res)

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

    def test_get(self, client, profile):
        res = client.put(url_for('api_app.profileresource'), data=profile)
        data = json.loads(res.data)

        res = client.get(url_for('api_app.profileresource', id=data['id']))

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

        profile['id'] = data['id']
        assert profile == data

    def test_delete(self, client, profile):
        res = client.put(url_for('api_app.profileresource'), data=profile)
        data = json.loads(res.data)

        res = client.delete(url_for('api_app.profileresource', id=data['id']))

        res = client.get(url_for('api_app.profileresource', id=data['id']))

        assert res.status_code == 404

    def test_post(self, client, profile):
        res = client.put(url_for('api_app.profileresource'), data=profile)
        data = json.loads(res.data)

        profile['profile_data'] = 'something else'
        res = client.post(url_for('api_app.profileresource', id=data['id']), data=profile)

        assert self.assert_success(res)

        res = client.get(url_for('api_app.profileresource', id=data['id']))

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        profile['id'] = data['id']
        assert data == profile
