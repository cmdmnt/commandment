import pytest
from commandment.dep.dep import DEP
from commandment.dep.errors import DEPError


class TestDEP:

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


    def test_account(self, dep: DEP):
        dep.fetch_token()
        account = dep.account()
        assert account is not None


