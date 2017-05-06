import pytest
from flask.testing import FlaskClient
from commandment import create_app
from commandment.models import db
from tests.client import MDMClient


@pytest.fixture()
def app() -> FlaskClient:
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
