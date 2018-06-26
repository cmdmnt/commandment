import pytest
import os.path
import logging
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from commandment.pki import openssl
import oscrypto

logger = logging.getLogger(__name__)


class TestOpenssl:

    def test_pkcs12_from_crypto(self, private_key: rsa.RSAPrivateKeyWithSerialization, certificate: x509.Certificate):
        pkcs12_data = openssl.create_pkcs12(private_key, certificate)


