import pytest
from flask import Flask
from commandment.app import create_app
from commandment.database import config_engine, init_db
import tempfile
import json
from . import JSON_API_HEADERS
from .fixtures import *


class TestApiCertificates:

    # def test_get_certificates(self, app):
    #     res = app.get('/api/v1/certificates/?size=50&number=1', headers=JSON_API_HEADERS)
    #     rd = json.loads(res.data)
    #     print(rd)
    #
    #     assert res.status_code == 200
    # def test_post_push_certificate(self, app):
    #     res = app.get('/api/v1/push_certificate', headers={
    #         'Content-Type': 'application/vnd.api+json',
    #         'Accept': 'application/vnd.api+json'
    #     })
    #
    # assert res.status_code == 201


    # def test_get_push_certificate(self, app):
    #     res = app.get('/api/v1/push_certificate', headers={
    #                 'Content-Type': 'application/vnd.api+json',
    #                 'Accept': 'application/vnd.api+json'
    #     })
    #     print(res.data)
    #     assert res.status_code == 200
        

    def test_post_certificate_signing_request(self, app):
        res = app.post('/api/v1/certificate_signing_requests', headers={
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
        }, data=json.dumps({
            'data': {
                'type': 'certificate_signing_requests',
                'attributes': {
                    'purpose': 'mdm.pushcert',
                    'subject': 'O=commandment/OU=IT/CN=commandment.dev'
                }
            }
        }))
        print(res.data)
        assert res.status_code == 201
