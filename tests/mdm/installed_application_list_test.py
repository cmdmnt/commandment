import pytest
import os
from flask import Response
from tests.client import MDMClient
from commandment.mdm import CommandStatus
from commandment.models import Command, Device

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def installed_application_list_response():
    with open(os.path.join(TEST_DIR, '../../testdata/InstalledApplicationList/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture(scope='function')
def installed_application_list_command(session):
    c = Command(
        uuid='00000000-1111-2222-3333-444455556666',
        request_type='InstalledApplicationList',
        status=CommandStatus.Sent.value,
        parameters={},
    )
    session.add(c)
    session.commit()


@pytest.mark.usefixtures("device", "installed_application_list_command")
class TestInstalledApplicationList:

    def test_installed_application_list_response(self, client: MDMClient, installed_application_list_response: str, session):
        response: Response = client.put('/mdm', data=installed_application_list_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200

        d: Device = session.query(Device).filter(Device.udid == '00000000-1111-2222-3333-444455556666').one()
        ia = d.installed_applications
        assert len(ia) == 3
