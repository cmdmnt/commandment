import datetime
from typing import Optional
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509 import NameOID, DNSName


def generate_signing_request(cn: str, dnsname: Optional[str] = None) -> (rsa.RSAPrivateKey, x509.CertificateSigningRequest):
    """Generate a Private Key + Certificate Signing Request using the given dnsname as the CN and SAN dNSName.
    
    Args:
            cn (str): The certificate common name
          dnsname (str): The public facing dns name of the MDM server.
    Returns:
          Tuple of rsa private key, csr
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
    ])

    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(name)

    if dnsname is not None:
        san = x509.SubjectAlternativeName([
            x509.DNSName(dnsname)
        ])
        builder = builder.add_extension(san, critical=True)

    builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    
    request = builder.sign(
        private_key,
        hashes.SHA256(),
        default_backend()
    )

    return private_key, request


def generate_self_signed_certificate(cn: str) -> (rsa.RSAPrivateKey, x509.Certificate):
    """Generate an X.509 Certificate with the given Common Name.
    
    Args:
          cn (string): 
    """
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
    ])

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    certificate = x509.CertificateBuilder().subject_name(
        name
    ).issuer_name(
        name
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            DNSName(cn)
        ]), False
    ).sign(private_key, hashes.SHA256(), default_backend())

    return private_key, certificate
