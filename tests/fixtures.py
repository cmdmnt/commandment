"""test_enrolment.py: Tests for enrolment behaviour"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import pytest
from fakeredis import FakeStrictRedis
from flask.ext.redis import FlaskRedis
import uuid
from commandment import app as capp, database
from commandment.models import ProfileStatus, Profile


@pytest.yield_fixture(scope="session")
def app():
    mock_redis = FlaskRedis.from_custom_provider(FakeStrictRedis)
    flask_app = capp.create_app(True, mock_redis)
    database.config_engine('sqlite://', echo=True)
    database.init_db()
    connection = database.engine.connect()

    yield flask_app

    connection.close()
    database.Base.metadata.drop_all(bind=database.engine)

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

@pytest.fixture
def device():
    device_uuid = str(uuid.uuid4())

    device = {
        'udid': device_uuid,
        'serial_number': '90210'
    }

    return device

@pytest.fixture
def mdm_group():
    group_uuid = str(uuid.uuid4())

    group = {
        'group_name': 'Group test ' + group_uuid,
        'description': 'Test group',
    }

    return group
