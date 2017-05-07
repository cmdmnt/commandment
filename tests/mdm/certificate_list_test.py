import pytest
import os
from flask import Response
from tests.client import MDMClient
from tests.fixtures import client

TEST_DIR = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture()
def certificate_list_response():
    with open(os.path.join(TEST_DIR, '../../testdata/CertificateList/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


class TestCertificateList:

    def test_certificate_list_response(self, client: MDMClient, certificate_list_response: str):
        response: Response = client.put('/mdm', data=certificate_list_response, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
