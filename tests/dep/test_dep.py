import pytest
from commandment.dep.dep import DEP


class TestDEP:

    def test_oauth(self, dep: DEP):
        t = dep.fetch_token()
