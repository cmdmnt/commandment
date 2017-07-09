import pytest
import os
from flask import Flask
from typing import Generator
from commandment import create_app
from commandment.models import db as _db, Device
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session
from tests.client import MDMClient

TEST_DIR = os.path.realpath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.realpath(TEST_DIR + '/../../testdata')


@pytest.fixture(scope='session')
def app() -> Generator[Flask, None, None]:
    """Flask Application Fixture"""
    a = create_app()
    a.config['TESTING'] = True
    ctx = a.app_context()
    ctx.push()

    yield a

    ctx.pop()


@pytest.fixture(scope='session')
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Flask-SQLAlchemy Fixture"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = False
    _db.init_app(app)
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db: SQLAlchemy) -> Generator[scoped_session, None, None]:
    """SQLAlchemy session Fixture"""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='function')
def client(app: Flask) -> MDMClient:
    """Flask test client"""
    app.test_client_class = MDMClient
    test_client = app.test_client()
    return test_client


@pytest.fixture(scope='function')
def device(session: scoped_session):
    d = Device(
        udid='00000000-1111-2222-3333-444455556666',
        device_name='commandment-mdmclient'
    )
    session.add(d)
    session.commit()


@pytest.fixture()
def authenticate_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'Authenticate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'TokenUpdate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_user_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'TokenUpdate/10.12.2-user.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def checkout_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'CheckOut/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data
