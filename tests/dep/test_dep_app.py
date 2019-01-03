import pytest
import os
import json
import sqlalchemy
from flask import Response

from commandment.dep.models import DEPProfile
from commandment.models import Device
from tests.client import MDMClient


@pytest.mark.dep
@pytest.mark.usefixtures("device", "dep_profile_committed")
class TestDEPAPI:

    def test_post_dep_profile_relationship(self, client: MDMClient, session):
        """Test assignment of DEP Profile to device via relationship URL:
            /api/v1/devices/<device_id>/relationships/dep_profiles"""
        request_json = json.dumps({
            "data": {
                "type": "dep_profiles",
                "id": "1",
            },
            "jsonapi": {
                "version": "1.0"
            }
        })

        response: Response = client.patch("/api/v1/devices/1/relationships/dep_profile", data=request_json,
                                          content_type="application/vnd.api+json")
        print(response.data)
        assert response.status_code == 200

        d: Device = session.query(Device).filter(Device.id == 1).one()
        assert d.dep_profile_id is not None
