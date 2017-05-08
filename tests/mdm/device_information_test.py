import pytest
import os
from flask import Response
from tests.client import MDMClient

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def device_information_response():
    with open(os.path.join(TEST_DIR, '../../testdata/DeviceInformation/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


class TestDeviceInformation:

    def test_device_information_response(self, client: MDMClient, device_information_response: str):
        response: Response = client.put('/mdm', data=device_information_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
