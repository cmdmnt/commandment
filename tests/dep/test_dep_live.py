import pytest
from commandment.dep.dep import DEP


@pytest.mark.dep
class TestDEPLive:
    def test_account(self, dep_live: DEP):
        dep_live.fetch_token()
        account = dep_live.account()
        assert account is not None
        assert 'server_name' in account
        assert 'server_uuid' in account
        assert 'facilitator_id' in account
        assert 'admin_id' in account
        assert 'org_name' in account
        assert 'org_email' in account
        assert 'org_phone' in account
        assert 'org_address' in account

        # X-Server-Protocol 3
        assert 'org_id' in account
        assert 'org_id_hash' in account
        assert 'org_type' in account
        assert 'org_version' in account
        
    def test_fetch_devices(self, dep_live: DEP):
        dep_live.fetch_token()
        devices = dep_live.fetch_devices()
        assert 'cursor' in devices
        assert 'devices' in devices
        assert 'fetched_until' in devices
        assert 'more_to_follow' in devices
        # assert len(devices['devices']) == 500
        
    # def test_device_details(self, dep: DEP):
    #     dep.fetch_token()
    #     device_details = dep.device_detail()

    # def test_fetch_cursor(self, dep: DEP):
    #     dep.fetch_token()
    #     for page in dep.devices():
    #         print(len(page))
    #         for d in page:
    #             print(d)

    def test_define_profile(self, dep: DEP, dep_profile: dict):
        result = dep.define_profile(dep_profile)
        assert 'profile_uuid' in result
        print(result['profile_uuid'])

    def test_list_profiles(self, dep: DEP):
        profiles = dep.profile()
        print(profiles)