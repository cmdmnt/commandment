import pytest
from flask import Response
from tests.client import MDMClient


class TestCheckin:

    def test_authenticate(self, client: MDMClient, authenticate_request: str):
        """Basic test: Authenticate"""
        response: Response = client.put('/checkin', data=authenticate_request, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
        
    def test_tokenupdate(self, client: MDMClient, tokenupdate_request: str):
        """Test a client attempting to update its token after being unenrolled."""
        response: Response = client.put('/checkin', data=tokenupdate_request, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200

    def test_user_tokenupdate(self, client: MDMClient, tokenupdate_user_request: str):
        """Test a TokenUpdate message on the user channel."""
        response: Response = client.put('/checkin', data=tokenupdate_user_request, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200

    def test_checkout(self, client: MDMClient, checkout_request: str):
        """Test a CheckOut message"""
        response: Response = client.put('/checkin', data=checkout_request, content_type='text/xml')
        assert response.status_code != 410
        assert response.status_code == 200
