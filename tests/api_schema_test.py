import pytest
from commandment.schema import CertificateSchema
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

class TestApiSchema:

    def test_certificate_dump(self):
        c = Certificate(cert_type='mdm.pushcert', subject='test')
        d = CertificateSchema().dump(c).data
        print(d)
