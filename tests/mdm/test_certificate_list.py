import pytest
import os
from flask import Response
from tests.client import MDMClient
from commandment.mdm import CommandStatus
from commandment.models import Command, Device

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def certificate_list_response():
    with open(os.path.join(TEST_DIR, '../../testdata/CertificateList/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture(scope='function')
def certificate_list_command(session):
    c = Command(
        uuid='00000000-1111-2222-3333-444455556666',
        request_type='CertificateList',
        status=CommandStatus.Sent.value,
        parameters={},
    )
    session.add(c)
    session.commit()


@pytest.mark.usefixtures("device", "certificate_list_command")
class TestCertificateList:

    def test_certificate_list_response(self, client: MDMClient, certificate_list_response: str, session):
        response: Response = client.put('/mdm', data=certificate_list_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200

        d = session.query(Device).filter(Device.udid == '00000000-1111-2222-3333-444455556666').one()
        ic = d.installed_certificates
        assert len(ic) == 2

