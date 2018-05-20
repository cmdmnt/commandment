import pytest
import os
import json
import sqlalchemy
from flask import Response
from tests.client import MDMClient
from commandment.models import Command


@pytest.mark.usefixtures("device")
class TestDevicesAPI:

    def test_patch_device_name(self, client: MDMClient, session):
        """Patching the device name should enqueue a Rename MDM command."""
        request_json = json.dumps({
            "data": {
                "type": "devices",
                "id": "1",
                "attributes": {
                    "device_name": "new name"
                }
            },
            "jsonapi": {
                "version": "1.0"
            }
        })

        response: Response = client.patch("/api/v1/devices/1", data=request_json,
                                          content_type="application/vnd.api+json")
        assert response.status_code == 200

        try:
            cmd: Command = session.query(Command).filter(Command.request_type == 'Settings').one()
        except sqlalchemy.orm.exc.NoResultFound:
            assert False, "The API has created a new Settings Command to send to the device"

        device = json.loads(response.data)
        assert device['data']['attributes']['device_name'] != "new name", "Device rename is still pending, API should reflect old name"

    @pytest.mark.skip
    def test_patch_hostname(self, client: MDMClient, session):
        """Patching the hostname should enqueue a Rename MDM command."""
        request_json = json.dumps({
            "data": {
                "type": "devices",
                "id": "1",
                "attributes": {
                    "hostname": "new name"
                }
            },
            "jsonapi": {
                "version": "1.0"
            }
        })

        response: Response = client.patch("/api/v1/devices/1", data=request_json,
                                          content_type="application/vnd.api+json")
        assert response.status_code == 200

        try:
            cmd: Command = session.query(Command).filter(Command.request_type == 'Settings').one()
        except sqlalchemy.orm.exc.NoResultFound:
            assert False, "The API has created a new Settings Command to send to the device"

        device = json.loads(response.data)
        assert device['data']['attributes']['hostname'] != "new name", "Device rename is still pending, API should reflect old name"

    def test_patch_hostname_ios(self):
        """Patching an iOS device hostname should return 400 bad request."""
        pass

    @pytest.mark.skip
    def test_patch_device_name_reverted(self, client: MDMClient, session):
        """Patching the device name twice (change, then back to its original name)
           should remove the queued Settings command."""
        request_json = json.dumps({
            "data": {
                "type": "devices",
                "id": "1",
                "attributes": {
                    "device_name": "new name"
                }
            },
            "jsonapi": {
                "version": "1.0"
            }
        })

        request_two_json = json.dumps({
            "data": {
                "type": "devices",
                "id": "1",
                "attributes": {
                    "device_name": "commandment-mdmclient"
                }
            },
            "jsonapi": {
                "version": "1.0"
            }
        })

        response: Response = client.patch("/api/v1/devices/1", data=request_json,
                                          content_type="application/vnd.api+json")
        assert response.status_code == 200

        second_response: Response = client.patch("/api/v1/devices/1", data=request_two_json,
                                          content_type="application/vnd.api+json")
        assert second_response.status_code == 200

        settings_commands = session.query(Command).filter(Command.request_type == 'Settings').count()
        assert settings_commands == 1

    def test_patch_device_name_coalesced(self, client: MDMClient, session):
            """Multiple device name changes should be coalesced into a single Settings command."""
            pass