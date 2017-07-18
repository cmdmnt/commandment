import pytest
from commandment.dep.dep import DEP


class TestDEP:
    def test_account(self, dep: DEP):
        dep.fetch_token()
        account = dep.account()
        assert account is not None

    def test_devices(self, dep: DEP):
        dep.fetch_token()
        devices = dep.devices()
        assert len(devices) == 500
        
    # def test_device_details(self, dep: DEP):
    #     dep.fetch_token()
    #     device_details = dep.device_detail()
