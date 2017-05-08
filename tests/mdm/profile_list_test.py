import pytest
import os
from flask import Response
from tests.client import MDMClient


TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def profile_list_response():
    with open(os.path.join(TEST_DIR, '../../testdata/ProfileList/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data

@pytest.mark.usefixtures("device")
class TestProfileList:

    def test_profile_list_response(self, client: MDMClient, profile_list_response: str):
        response: Response = client.put('/mdm', data=profile_list_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
