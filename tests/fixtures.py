import pytest
import os
from flask.testing import FlaskClient
from commandment import create_app
from commandment.models import db
from tests.client import MDMClient

TEST_DIR = os.path.realpath(os.path.dirname(__file__))

@pytest.fixture(scope='session')
def client() -> MDMClient:
    a = create_app()
    a.test_client_class = MDMClient
    a.config['TESTING'] = True
    a.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    a.config['SQLALCHEMY_ECHO'] = False

    with a.app_context():
        db.init_app(a)
        db.create_all()

    test_client = a.test_client()
    return test_client


@pytest.fixture()
def authenticate_request() -> str:
    with open(os.path.join(TEST_DIR, '../testdata/Authenticate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_request() -> str:
    with open(os.path.join(TEST_DIR, '../testdata/TokenUpdate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_user_request() -> str:
    with open(os.path.join(TEST_DIR, '../testdata/TokenUpdate/10.12.2-user.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def checkout_request() -> str:
    with open(os.path.join(TEST_DIR, '../testdata/CheckOut/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data
