import pytest
from commandment.dep.dep import DEP
from commandment.dep.errors import DEPError

@pytest.mark.depsim
class TestDEPFailures:
    # NOTE: ensure that this is in exactly the same order as your DEPsim config.
    @pytest.mark.parametrize("expected_status,expected_text", [
        (400, ""),
        (403, "ACCESS_DENIED"),
        (403, "T_C_NOT_SIGNED"),
        (405, ""),
        (401, "UNAUTHORIZED"),
        (429, "TOO_MANY_REQUESTS"),
    ])
    def test_token_failure(self, dep: DEP, expected_status: int, expected_text: str):
        try:
            dep.fetch_token()
        except DEPError as e:
            assert e.response.status_code == expected_status
            assert e.text == expected_text

    @pytest.mark.parametrize("expected_status,expected_text", [
        (403, "ACCESS_DENIED"),
        (401, "UNAUTHORIZED"),
    ])
    def test_account_failure(self, dep: DEP, expected_status: int, expected_text: str):
        try:
            dep.fetch_token()
            dep.account()
        except DEPError as e:
            assert e.response.status_code == expected_status
            assert e.text == expected_text


