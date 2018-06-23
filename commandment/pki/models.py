"""
This module contains the SQLAlchemy models for PKI related functionality.
"""

from commandment.models import db, CertificateSigningRequest, CertificateType, DeviceIdentityCertificate, CACertificate, RSAPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509 import NameOID, DNSName
import datetime


class CertificateAuthority(db.Model):
    """Certificate authority storage: database implementation.

    I'm loathe to create a model tied to the storage implementation but this was the easiest option at the time.
    """
    __tablename__ = 'certificate_authority'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String, unique=True)
    serial = db.Column(db.Integer, default=0)
    validity_period = db.Column(db.Integer, default=365)

    certificate_id = db.Column(db.Integer, db.ForeignKey('certificates.id'))
    certificate = db.relationship('CACertificate', backref='certificate_authority')

    rsa_private_key_id = db.Column(db.Integer, db.ForeignKey('rsa_private_keys.id'))
    rsa_private_key = db.relationship('RSAPrivateKey', backref='certificate_authority')

    @classmethod
    def create(cls, common_name: str = 'COMMANDMENT-CA', key_size=2048):
        ca = cls()
        ca.common_name = common_name
        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
        ])

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend(),
        )
        ca.rsa_private_key = RSAPrivateKey.from_crypto(private_key)

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
            x509.BasicConstraints(ca=True, path_length=None), True
        ).sign(ca.private_key, hashes.SHA256(), default_backend())

        ca.certificate = CACertificate.from_crypto(certificate)

        db.session.add(ca)
        db.session.commit()

        return ca

    def create_device_csr(self, common_name: str) -> (rsa.RSAPrivateKeyWithSerialization, x509.CertificateSigningRequest):
        """
        Create a Certificate Signing Request with the specified Common Name.

        The private key model is automatically committed to the database.
        This is also true for the certificate signing request.

        Args:
            common_name (str): The certificate Common Name attribute

        Returns:
            Tuple[rsa.RSAPrivateKeyWithSerialization, x509.CertificateSigningRequest] - A tuple containing the RSA
            Private key that was generated, along with the CSR.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )

        private_key_model = RSAPrivateKey.from_crypto(private_key)
        db.session.add(private_key_model)
        db.session.commit()

        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
        ])

        builder = x509.CertificateSigningRequestBuilder()
        builder = builder.subject_name(name)
        builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)

        request = builder.sign(
            private_key,
            hashes.SHA256(),
            default_backend()
        )

        csr_model = CertificateSigningRequest().from_crypto(request)
        db.session.add(csr_model)
        db.session.commit()

        return private_key, request

    def sign(self, request: x509.CertificateSigningRequest) -> x509.Certificate:
        """
        Sign a Certificate Signing Request.

        The issued certificate is automatically persisted to the database.

        Args:
            request (x509.CertificateSigningRequest): The CSR object (cryptography) not the SQLAlchemy model.

        Returns:
            x509.Certificate: A signed certificate
        """
        b = x509.CertificateBuilder()
        self.serial += 1

        cert = b.not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + self.validity_period
        ).serial_number(
            self.serial
        ).issuer_name(
            self.name
        ).subject_name(
            request.subject
        ).sign(self.private_key, hashes.SHA256(), default_backend())

        cert_model = DeviceIdentityCertificate().from_crypto(cert)
        db.session.add(cert_model)
        db.session.commit()

        return cert
