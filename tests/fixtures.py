"""test_enrolment.py: Tests for enrolment behaviour"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import pytest
from mockredis import MockRedis
from flask.ext.redis import FlaskRedis
from commandment import app as capp, database


class MockRedisWrapper(MockRedis):
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


@pytest.yield_fixture(scope="session")
def app():
    mock_redis = FlaskRedis.from_custom_provider(MockRedisWrapper)
    flask_app = capp.create_app(True, mock_redis)
    database.config_engine('sqlite://', echo=True)
    database.init_db()
    connection = database.engine.connect()

    yield flask_app

    connection.close()
    database.Base.metadata.drop_all(bind=database.engine)
