import pytest
from commandment.dep.dep import DEP


class TestDEP:

    def test_oauth(self, dep: DEP):
        token = dep.fetch_token()
        assert token is not None

    def test_account(self, dep: DEP):
        dep.fetch_token()
        account = dep.account()
        assert account is not None


