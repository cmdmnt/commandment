import pytest
import os.path
import logging
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from commandment.models import RSAPrivateKey, CACertificate

logger = logging.getLogger(__name__)


class TestModels:

    def test_rsa_privatekey_from_crypto(self, private_key: rsa.RSAPrivateKeyWithSerialization, session):
        m = RSAPrivateKey.from_crypto(private_key)
        session.add(m)
        session.commit()

        assert m.id is not None
        assert m.pem_data is not None

    def test_ca_certificate_from_crypto(self, ca_certificate: x509.Certificate, session):
        m = CACertificate.from_crypto(ca_certificate)
        session.add(m)
        session.commit()

        assert m.id is not None
        assert m.pem_data is not None
        assert m.fingerprint is not None
        assert m.x509_cn is not None

