import pytest
from flask.testing import FlaskClient
from flask import Response
from tests.fixtures import app


class TestCheckin:

    def test_authenticate(self, app: FlaskClient):
        """Basic test: Authenticate"""
        with open('../../testdata/Authenticate/10.12.2.xml', 'r') as fd:
            plist_data = fd.read()
            
        response: Response = app.put('/checkin', data=plist_data, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
        
    def test_tokenupdate(self, app: FlaskClient):
        """Test a client attempting to update its token after being unenrolled."""
        with open('../../testdata/TokenUpdate/10.12.2.xml', 'r') as fd:
            plist_data = fd.read()

        response: Response = app.put('/checkin', data=plist_data, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200


