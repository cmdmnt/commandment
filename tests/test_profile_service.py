"""test_profile_service.py: Tests for the service class providing general profile support"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import sys
import pytest
import json
import sqlalchemy
import sqlalchemy.orm
import uuid
import werkzeug
import mock
from utils import get_queued_jobs
from commandment import database as cdatabase
from commandment.models import Profile, MDMGroup, ProfileStatus, Device
from commandment.profiles import service
from flask import url_for

from fixtures import app, profile, device


class TestProfileService:
    def test_install_queues_a_job_only_if_status_is_inactive(self, profile, app):
        profile = Profile(**profile)
        profile_server = service.ProfileService()

        redis_client = app.redis_store._redis_client

        for status in list(ProfileStatus):
            redis_client.flushall()
            profile.id = 1
            profile.status = status
            try:
                profile_server.install(profile)
            except werkzeug.exceptions.BadRequest as e:
                bad_request = True
            else:
                bad_request = False

            if status == ProfileStatus.INACTIVE:
                assert profile.status == ProfileStatus.PENDING_INSTALLATION
                assert get_queued_jobs(redis_client) == ['commandment.tasks.process_profile_deployment_change(%d)' % profile.id]
                assert not bad_request
            elif status == ProfileStatus.ACTIVE:
                assert profile.status == ProfileStatus.ACTIVE
                assert get_queued_jobs(redis_client) == []
                assert not bad_request
            else:
                assert profile.status == status
                assert get_queued_jobs(redis_client) == []
                assert bad_request

    def test_remove_queues_a_job_only_if_status_is_active(self, profile, app):
        profile = Profile(**profile)
        profile_server = service.ProfileService()

        redis_client = app.redis_store._redis_client

        for status in list(ProfileStatus):
            redis_client.flushall()
            profile.id = 1
            profile.status = status
            try:
                profile_server.remove(profile)
            except werkzeug.exceptions.BadRequest as e:
                bad_request = True
            else:
                bad_request = False

            if status == ProfileStatus.ACTIVE:
                assert profile.status == ProfileStatus.PENDING_REMOVAL
                assert get_queued_jobs(redis_client) == ['commandment.tasks.process_profile_deployment_change(%d)' % profile.id]
                assert not bad_request
            elif status == ProfileStatus.INACTIVE:
                assert profile.status == ProfileStatus.INACTIVE
                assert get_queued_jobs(redis_client) == []
                assert not bad_request
            else:
                assert profile.status == status
                assert get_queued_jobs(redis_client) == []
                assert bad_request

    def test_finalize_installation(self, profile, device):
        profile = Profile(**profile)
        device = Device(**device)
        profile_service = service.ProfileService()
        profile.id = 7

        service.db_session = mock.MagicMock()
        query = mock.MagicMock()
        service.db_session.query.return_value = query
        query.get.return_value = profile

        installqc = object()
        service.InstallProfile = mock.MagicMock()
        service.InstallProfile.new_queued_command.return_value = installqc

        service.db_session.add = mock.MagicMock()

        profile_service.finalize_installation(profile, device)

        assert service.InstallProfile.new_queued_command.call_args[0] == (device, {'id': 7})
        service.db_session.add.assert_called_once_with(installqc)

    def test_finalize_removal(self, profile, device):
        profile = Profile(**profile)
        device = Device(**device)
        profile_service = service.ProfileService()

        service.db_session = mock.MagicMock()
        query = mock.MagicMock()
        service.db_session.query.return_value = query
        query.get.return_value = profile

        removeqc = object()
        service.RemoveProfile = mock.MagicMock()
        service.RemoveProfile.new_queued_command.return_value = removeqc

        service.db_session.add = mock.MagicMock()

        profile_service.finalize_removal(profile, device)

        assert service.RemoveProfile.new_queued_command.call_args[0] == (device, {'Identifier': profile.identifier, 'UUID': profile.uuid})
        service.db_session.add.assert_called_once_with(removeqc)
