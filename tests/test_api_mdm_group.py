"""test_api_mdm_group.py: Tests for API group access"""

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

@pytest.yield_fixture(scope="session")
def app():
    app = capp.create_app(debug=True)
    cdatabase.config_engine('sqlite://', echo=True)
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

    def test_get_by_name(self, client, mdm_group):
        mdm_group = MDMGroup(**mdm_group)

        cdatabase.db_session.add(mdm_group)
        cdatabase.db_session.commit()

        res = client.get(url_for('api_app.mdmgroupresource'), data={'group_name': mdm_group.group_name})

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        assert len(data) == 1
        assert data[0]['id'] == mdm_group.id

    def test_put(self, client, group):
        res = client.put(url_for('api_app.groupresource'), data=group)
        assert self.assert_json(res.headers)
        assert self.assert_success(res)

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

    def test_get(self, client, group):
        res = client.put(url_for('api_app.groupresource'), data=group)
        data = json.loads(res.data)

        res = client.get(url_for('api_app.groupresource', id=data['id']))

        data = json.loads(res.data)

        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0

        group['id'] = data['id']
        assert group == data

    def test_delete(self, client, group):
        res = client.put(url_for('api_app.groupresource'), data=group)
        data = json.loads(res.data)

        res = client.delete(url_for('api_app.groupresource', id=data['id']))

        res = client.get(url_for('api_app.groupresource', id=data['id']))

        assert res.status_code == 404

    def test_post(self, client, group):
        res = client.put(url_for('api_app.groupresource'), data=group)
        data = json.loads(res.data)

        group['group_name'] = 'something else'
        res = client.post(url_for('api_app.groupresource', id=data['id']), data=group)

        assert self.assert_success(res)

        res = client.get(url_for('api_app.groupresource', id=data['id']))

        assert self.assert_json(res.headers)
        assert self.assert_success(res)
        data = json.loads(res.data)

        group['id'] = data['id']
        assert data == group
