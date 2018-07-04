import pytest
import os.path
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from commandment.dep import smime

DEP_TOKEN_SMIME_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'dep_smime.p7m')
DEP_TOKEN_KEY_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'dep_key.pem')


class TestDepSmime:
    def test_decrypt(self):
        with open(DEP_TOKEN_SMIME_PATH, 'rb') as fd:
            message = fd.read()

        with open(DEP_TOKEN_KEY_PATH, 'rb') as fd:
            pem_key = fd.read()

        pk = serialization.load_pem_private_key(
            pem_key,
            backend=default_backend(),
            password=None,
        )

        result = smime.decrypt(message, pk)
        print(result)
