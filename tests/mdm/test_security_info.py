import pytest
import os
from flask import Response

from commandment.mdm import CommandStatus
from tests.client import MDMClient
from commandment.models import Command, Device

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def security_info_response():
    with open(os.path.join(TEST_DIR, '../../testdata/SecurityInfo/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture(scope='function')
def security_info_command(session):
    c = Command(
        uuid='00000000-1111-2222-3333-444455556666',
        request_type='SecurityInfo',
        status=CommandStatus.Sent.value,
        parameters={},
    )
    session.add(c)
    session.commit()


@pytest.mark.usefixtures("device", "security_info_command")
class TestSecurityInfo:

    def test_security_info_response(self, client: MDMClient, security_info_response: str, session):
        response: Response = client.put('/mdm', data=security_info_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200

        cmd = session.query(Command).filter(Command.uuid == '00000000-1111-2222-3333-444455556666').one()
        assert CommandStatus(cmd.status) == CommandStatus.Acknowledged

        d = session.query(Device).filter(Device.udid == '00000000-1111-2222-3333-444455556666').one()
        assert not d.fde_enabled