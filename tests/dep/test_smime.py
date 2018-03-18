import pytest
import os.path
from commandment.dep import smime

DEP_TOKEN_SMIME_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'stoken.p7m')


class TestDepSmime:
    def test_load(self):
        result = smime.decrypt(DEP_TOKEN_SMIME_PATH)
