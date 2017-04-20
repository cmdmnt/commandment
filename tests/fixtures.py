import pytest
import os
from commandment.app import create_app
from commandment.database import config_engine, init_db
from commandment.models import Certificate

P12_FIXTURE = os.path.join(os.path.dirname(__file__), 'push.p12')


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

@pytest.fixture()
def pkcs12_certificate() -> bytes:
    with open(P12_FIXTURE, 'rb') as fd:
        data = fd.read()

    return data

