import pytest
import os.path
import logging
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

ENCRYPTION_CERT = os.path.join(os.path.dirname(__file__), '..', 'commandment.crt')

logger = logging.getLogger(__name__)

@pytest.fixture
def private_key() -> rsa.RSAPrivateKey:
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    return key


@pytest.fixture
def csr(private_key: rsa.RSAPrivateKey) -> x509.CertificateSigningRequest:
    b = x509.CertificateSigningRequestBuilder()
    req = b.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Commandment"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"Commandment"),
    ])).sign(private_key, hashes.SHA256(), default_backend())

    return req


@pytest.fixture
def encryption_cert() -> x509.Certificate:
    with open(ENCRYPTION_CERT, 'rb') as fd:
        certdata = fd.read()

    cert = x509.load_pem_x509_certificate(certdata, default_backend())
    return cert


class TestMDMCert:
    pass
    # def test_submit_mdmcert_request(self, csr: x509.CertificateSigningRequest, encryption_cert: x509.Certificate):
    #     res = submit_mdmcert_request("admin@localhost", csr, encryption_cert)
    #     assert res['result'] == 'success'
