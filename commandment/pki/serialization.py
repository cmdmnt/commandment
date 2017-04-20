from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from asn1crypto import pkcs12, pem, x509 as asn1x509


# cryptography helper functions

def from_pem(pem_data: str) -> x509.Certificate:
    return x509.load_pem_x509_certificate(pem_data, default_backend())


def from_der(der_data: bytes) -> x509.Certificate:
    return x509.load_der_x509_certificate(der_data, default_backend())


def rsa_from_der(rsa_der_data: bytes, password: str = None) -> rsa.RSAPrivateKeyWithSerialization:
    return serialization.load_der_private_key(
        rsa_der_data,
        password,
        default_backend()
    )


def rsa_from_pem(rsa_pem_data: bytes, password: str = None) -> rsa.RSAPrivateKeyWithSerialization:
    return serialization.load_pem_private_key(
        rsa_pem_data,
        password,
        default_backend()
    )


def rsa_to_pem(key: rsa.RSAPrivateKeyWithSerialization) -> str:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def to_pem(certificate: x509.Certificate) -> str:
    """Convert an instance of x509.Certificate to a PEM string
    
    Args:
          certificate (x509.Certificate): Cert to convert
    Returns:
          PEM string
    """
    serialized = certificate.public_bytes(
        encoding=serialization.Encoding.PEM
    )

    return serialized


def to_der(certificate: x509.Certificate) -> bytes:
    """Convert an instance of x509.Certificate to DER bytes
    
    Args:
          certificate (x509.Certificate): Cert to convert
    Returns:
          DER bytes    
    """
    serialized = certificate.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return serialized
