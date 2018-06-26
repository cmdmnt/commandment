import pytest
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


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
def certificate(private_key: rsa.RSAPrivateKey) -> x509.Certificate:
    b = x509.CertificateBuilder()
    name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Commandment"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"CA-CERTIFICATE"),
    ])

    cer = b.subject_name(name).issuer_name(name).public_key(
        private_key.public_key()
    ).serial_number(1).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), True
    ).sign(private_key, hashes.SHA256(), default_backend())

    return cer


@pytest.fixture
def ca_certificate(private_key: rsa.RSAPrivateKey) -> x509.Certificate:
    b = x509.CertificateBuilder()
    name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Commandment"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"CA-CERTIFICATE"),
    ])

    cert = b.serial_number(1).issuer_name(
        name
    ).subject_name(
        name
    ).public_key(
        private_key.public_key()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), True
    ).sign(private_key, hashes.SHA256(), default_backend())

    return cert

