from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime


def generate_csr(private_key: rsa.RSAPrivateKey = None):
    """Generate a Certificate Signing Request using a few defaults.

    Args:
          private_key (rsa.RSAPrivateKey): Optional. If not supplied a key will be generated

    Returns:
          Tuple of private_key, x509.CertificateSigningRequest
    """
    if private_key is None:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        
    builder = x509.CertificateSigningRequestBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'scepy client'),
    ]))
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=False), critical=True
    )
    csr = builder.sign(
        private_key, hashes.SHA256(), default_backend()
    )
    return private_key, csr


def generate_self_signed(private_key: rsa.RSAPrivateKey, subject: x509.Name) -> x509.Certificate:
    """Generate a Self-Signed certificate for use with a CMS PKCS#10 request.

    Args:
          private_key (rsa.RSAPrivateKey): The private key to sign the certificate with.
        subject (x509.Name): The subject used in the CSR, which must match this certificates subject.

    Returns:
          x509.Certificate: Self signed certificate for CMS envelope
    """
    one_day = datetime.timedelta(1, 0, 0)
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(subject)
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime(2018, 1, 1))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(private_key.public_key())
    builder = builder.add_extension(
        x509.KeyUsage(digital_signature=True, key_encipherment=True), critical=True
    )
    certificate = builder.sign(private_key=private_key, algorithm=hashes.SHA256(),
                               backend=default_backend())
    return certificate

