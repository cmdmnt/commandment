import pytest
from flask import Flask
from commandment.app import create_app
import tempfile
import json


@pytest.fixture()
def app():
    a = create_app()
    a.config['TESTING'] = True
    a.config['DATABASE'] = tempfile.mkstemp()
    test_client = a.test_client()
    yield test_client
    print('teardown')  # TODO: DB removal


class TestApi:
    def test_new_csr(self, app):
        res = app.post('/api/v1/certificate_signing_requests', headers={
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
        }, data=json.dumps({
            'data': {
                'type': 'certificate_signing_request',
                'attributes': {
                    'purpose': 'mdm.pushcert',
                    'subject': 'O=commandment/OU=IT'
                }
            }
        }))
        print(res.data)
        assert res.status_code == 201
