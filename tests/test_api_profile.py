"""test_api_profile.py: Tests for API profile access"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import sys
import pytest
import json
import sqlalchemy
import sqlalchemy.orm
import uuid
from utils import get_queued_jobs
from commandment import database as cdatabase
from commandment.models import Profile, MDMGroup, ProfileStatus
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
        'profile_data': '',
        'status': ProfileStatus.INACTIVE
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

        assert data['identifier'] == profile['identifier']
        assert data['uuid'] == profile['uuid']
        assert data['status'] == profile['status'].value

    def test_delete(self, client, profile):
        profile_dict = profile
        for status in list(ProfileStatus):
            profile = Profile(**profile_dict)
            profile.status = status
            cdatabase.db_session.add(profile)
            cdatabase.db_session.commit()
            profile_id = profile.id

            res = client.delete(url_for('api_app.profileresource', id=profile_id))

            res = client.get(url_for('api_app.profileresource', id=profile_id))
            assert self.assert_json(res.headers)

            deleted = False
            if status == ProfileStatus.ACTIVE:
                assert self.assert_success(res)
                assert profile.status == ProfileStatus.PENDING_DELETION
            elif status == ProfileStatus.INACTIVE:
                assert res.status_code == 404
                deleted = True
            else:
                assert profile.status == status

            if not deleted:
                cdatabase.db_session.delete(profile)
                cdatabase.db_session.commit()

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

        assert data['identifier'] == profile['identifier']
        assert data['uuid'] == profile['uuid']
        assert data['status'] == profile['status'].value

    def test_deploy_works_only_if_inactive(self, client, profile, app):
        profile = Profile(**profile)

        cdatabase.db_session.add(profile)
        cdatabase.db_session.commit()

        redis_client = app.redis_store._redis_client

        for status in list(ProfileStatus):
            redis_client.flushall()
            profile.status = status
            cdatabase.db_session.commit()
            res = client.put(url_for('api_app.profileresource_deploy', id=profile.id))
            assert self.assert_json(res.headers)

            if status == ProfileStatus.INACTIVE:
                assert self.assert_success(res)
                assert profile.status == ProfileStatus.PENDING_INSTALLATION
                assert get_queued_jobs(redis_client) == ['commandment.tasks.process_profile_deployment_change(%d)' % profile.id]
            elif status == ProfileStatus.ACTIVE:
                assert self.assert_success(res)
                assert profile.status == ProfileStatus.ACTIVE
                assert get_queued_jobs(redis_client) == []
            else:
                assert res.status_code == 400
                assert profile.status == status
                assert get_queued_jobs(redis_client) == []

    def test_undeploy_works_only_if_active(self, client, profile, app):
        profile = Profile(**profile)

        redis_client = app.redis_store._redis_client

        cdatabase.db_session.add(profile)
        cdatabase.db_session.commit()

        for status in list(ProfileStatus):
            redis_client.flushall()
            profile.status = status
            cdatabase.db_session.commit()
            res = client.delete(url_for('api_app.profileresource_deploy', id=profile.id))
            assert self.assert_json(res.headers)

            if status == ProfileStatus.ACTIVE:
                assert self.assert_success(res)
                assert profile.status == ProfileStatus.PENDING_REMOVAL
                assert get_queued_jobs(redis_client) == ['commandment.tasks.process_profile_deployment_change(%d)' % profile.id]
            elif status == ProfileStatus.INACTIVE:
                assert self.assert_success(res)
                assert profile.status == ProfileStatus.INACTIVE
                assert get_queued_jobs(redis_client) == []
            else:
                assert res.status_code == 400
                assert profile.status == status
                assert get_queued_jobs(redis_client) == []
