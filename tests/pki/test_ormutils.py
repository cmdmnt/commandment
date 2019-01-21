import pytest
import os.path
import logging
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from commandment.pki.models import RSAPrivateKey, CACertificate


logger = logging.getLogger(__name__)


class TestORMUtils:

    def test_find_recipient(self, certificate):
        pass
