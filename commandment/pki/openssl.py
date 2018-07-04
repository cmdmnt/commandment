# Regrettably, some functionality must come from PyOpenSSL
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.hazmat.primitives import serialization
import OpenSSL


def create_pkcs12(
        private_key: rsa.RSAPrivateKeyWithSerialization,
        certificate: x509.Certificate,
        passphrase: Optional[str] = None) -> Optional[bytes]:
    """Create a PKCS#12 container from the given RSA key and Certificate."""

    p12 = OpenSSL.crypto.PKCS12()
    pkey = OpenSSL.crypto.PKey.from_cryptography_key(private_key)
    p12.set_privatekey(pkey)
    cert = OpenSSL.crypto.X509.from_cryptography(certificate)
    p12.set_certificate(cert)

    return p12.export(passphrase)

