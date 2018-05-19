import pytest
import os
from flask import Flask
from typing import Generator
from commandment import create_app
from commandment.models import db as _db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from tests.client import MDMClient
from alembic.command import upgrade
from alembic.config import Config

# For testing, every test uses an in-memory database with migrations that are applied in the fixture setup phase.
# This ensures every test is fully isolated.

TEST_DATABASE_URI = 'sqlite:////tmp/test.db'
TEST_DIR = os.path.realpath(os.path.dirname(__file__))
ALEMBIC_CONFIG = os.path.realpath(TEST_DIR + '/alembic_test.ini')
TEST_APP_CONFIG = os.path.realpath(TEST_DIR + '/../travis-ci-settings.cfg')


def apply_migrations(connection):
    """Applies all Alembic migrations."""
    config = Config(ALEMBIC_CONFIG)

    # Issues with running upgrade() in a fixture with SQLite in-memory:
    # https://github.com/miguelgrinberg/Flask-Migrate/issues/153
    # Basically: Alembic always spawns a new connection from upgrade() unless you specify a connection
    # in config.attributes['connection']
    config.attributes['connection'] = connection
    upgrade(config, 'head')


@pytest.yield_fixture(scope='function')
def app() -> Generator[Flask, None, None]:
    """Flask Application Fixture"""
    a = create_app(TEST_APP_CONFIG)
    a.config['TESTING'] = True
    a.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    ctx = a.app_context()
    ctx.push()
    yield a
    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Flask-SQLAlchemy Fixture"""
    _db.app = app
    # _db.init_app(app)
    #_db.create_all()
    yield _db
    # _db.drop_all()


@pytest.yield_fixture(scope='function')
def session(db: SQLAlchemy) -> Generator[scoped_session, None, None]:
    """SQLAlchemy session Fixture"""
    connection = _db.engine.connect()
    # transaction = connection.begin()

    apply_migrations(connection)
    options = dict(bind=connection) #  , binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    # transaction.rollback()
    session.remove()


@pytest.fixture(scope='function')
def client(app: Flask) -> MDMClient:
    """Flask test client"""
    app.test_client_class = MDMClient
    test_client = app.test_client()
    return test_client

