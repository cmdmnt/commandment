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

    key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    p12.set_privatekey(key_bytes)

    certificate_bytes = certificate.public_bytes(
        encoding=serialization.Encoding.DER
    )

    p12.set_certificate(certificate_bytes)

    return p12.export(passphrase)

