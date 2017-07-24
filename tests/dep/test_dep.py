import pytest
from commandment.dep.dep import DEP


@pytest.mark.depsim
class TestDEP:
    def test_account(self, dep: DEP):
        dep.fetch_token()
        account = dep.account()
        assert account is not None

    def test_fetch_devices(self, dep: DEP):
        dep.fetch_token()
        devices = dep.fetch_devices()
        assert len(devices) == 500
        
    # def test_device_details(self, dep: DEP):
    #     dep.fetch_token()
    #     device_details = dep.device_detail()

    def test_fetch_cursor(self, dep: DEP):
        dep.fetch_token()
        for page in dep.devices():
            print(len(page))
            for d in page:
                print(d)

