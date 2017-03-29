import pytest
from commandment.app import create_app
from commandment.database import config_engine, init_db
from commandment.models import Certificate


@pytest.fixture()
def app():
    a = create_app()
    a.config['TESTING'] = True
    config_engine('sqlite:///:memory:', True)
    init_db()

    test_client = a.test_client()
    yield test_client
    print('teardown')  # TODO: DB removal

@pytest.fixture()
def certificate():
    c = Certificate(cert_type='mdm.pushcert', subject='test.host.name')
    return c

