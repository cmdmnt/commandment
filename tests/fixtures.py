import pytest
from commandment import create_app
from commandment.models import db


@pytest.fixture()
def app():
    a = create_app()
    a.config['TESTING'] = True
    a.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    a.config['SQLALCHEMY_ECHO'] = True
    db.init_app(a)
    db.Base.create_all()

    test_client = a.test_client()
    return test_client
