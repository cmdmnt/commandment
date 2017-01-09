"""test_tasks.py: Tests for rq worker"""

import uuid
import pytest
from mock import MagicMock
from commandment import tasks
from commandment.models import Profile, ProfileStatus, MDMGroup, Device
from fixtures import profile, mdm_group, device

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"


class TestProcessProfileDeploymentChanged:
    def test_deploy_changes_iff_status_is_correct_pending(self, profile, mdm_group, device):
        profile = Profile(**profile)
        mdm_group = MDMGroup(**mdm_group)
        device = Device(**device)
        profile_service = MagicMock()

        profile.mdm_groups = [mdm_group]
        mdm_group.devices = [device]

        tasks.ProfileService = MagicMock()
        tasks.ProfileService.return_value = profile_service
        tasks.db_session = MagicMock()
        query = MagicMock()
        tasks.db_session.query.return_value = query
        query.get.return_value = profile

        for status in list(ProfileStatus):
            profile.status = status
            tasks.push_to_device = MagicMock()
            tasks.db_session.add = MagicMock()

            tasks.process_profile_deployment_change(7)

            if status == ProfileStatus.PENDING_INSTALLATION:
                assert profile.status == ProfileStatus.ACTIVE
                tasks.push_to_device.assert_called_once_with(device)
            elif status == ProfileStatus.PENDING_DELETION:
                assert profile.status == ProfileStatus.PENDING_DELETION
                tasks.push_to_device.assert_called_once_with(device)
            elif status == ProfileStatus.PENDING_REMOVAL:
                assert profile.status == ProfileStatus.INACTIVE
                tasks.push_to_device.assert_called_once_with(device)
            else:
                assert profile.status == status
                assert not tasks.push_to_device.called
