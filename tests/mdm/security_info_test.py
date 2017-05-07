import pytest
import os
from flask import Response
from tests.client import MDMClient
from tests.fixtures import client

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def security_info_response():
    with open(os.path.join(TEST_DIR, '../../testdata/SecurityInfo/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


class TestSecurityInfo:

    def test_security_info_response(self, client: MDMClient, security_info_response: str):
        response: Response = client.put('/mdm', data=security_info_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
