import pytest
from commandment.dep.dep import DEP
from commandment.dep.errors import DEPError


class TestDEP:
    def test_account(self, dep: DEP):
        dep.fetch_token()
        account = dep.account()
        assert account is not None

    def test_devices(self, dep: DEP):
        dep.fetch_token()
        devices = dep.devices()
        assert len(devices) == 500
        

