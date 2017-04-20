import pytest
from flask import Flask
from commandment.app import create_app
import tempfile


@pytest.fixture()
def app():
    a = create_app()
    a.config['TESTING'] = True
    a.config['DATABASE'] = tempfile.mkstemp()
    test_client = a.test_client()
    yield test_client
    print('teardown')  # TODO: DB removal


class TestAdminBlueprint:
    def test_index(self, app):
        res = app.get('/admin/')
        assert res.status_code == 200

    def test_certificates(self, app):
        res = app.get('/admin/certificates')
        assert res.status_code == 200

    def test_groups(self, app):
        res = app.get('/admin/groups')
        assert res.status_code == 200

