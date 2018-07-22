"""
This module contains the SQLAlchemy models for PKI related functionality.
"""
from enum import Enum

from commandment.models import db
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
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
        db.session.add(ca.rsa_private_key)

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
        ).sign(private_key, hashes.SHA256(), default_backend())

        ca_certificate_model = CACertificate.from_crypto(certificate)
        ca_certificate_model.rsa_private_key = ca.rsa_private_key
        ca.certificate = ca_certificate_model

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
        csr_model.rsa_private_key = private_key_model
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

        private_key_model = self.rsa_private_key
        private_key = private_key_model.to_crypto()
        # ca_certificate_model = self.certificate
        # ca_certificate = ca_certificate_model.to_crypto()

        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
        ])

        cert = b.not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=self.validity_period)
        ).serial_number(
            self.serial
        ).issuer_name(
            name
        ).subject_name(
            request.subject
        ).public_key(
            request.public_key()
        ).sign(private_key, hashes.SHA256(), default_backend())

        # cert_model = DeviceIdentityCertificate().from_crypto(cert)
        # db.session.add(cert_model)
        # db.session.commit()

        return cert


class CertificateType(Enum):
    """A list of the polymorphic identities available for subclasses of Certificate.

    The enumerated type hints what the certificate is intended to be used for.
    """
    CSR = 'csr'
    PUSH = 'mdm.pushcert'
    ENCRYPT = 'mdm.encrypt'
    WEB = 'mdm.webcrt'
    CA = 'mdm.cacert'
    DEVICE = 'mdm.device'
    STOKEN = 'dep.stoken'
    ANCHOR = 'dep.anchor'
    SUPERVISION = 'dep.supervision'

class Certificate(db.Model):
    """Polymorphic base for certificate types.

    These certificate classes are only intended to be used for storing certificates related to running the MDM or
    certificates issued by the MDM internal CA or SCEP service.

    Note that X.509 name attributes have fixed lengths as defined in `RFC5280`_.

    :table: certificates

    .. _RFC5280:
       http://www.ietf.org/rfc/rfc5280.txt
    """
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    """id (int): Primary Key"""
    pem_data = db.Column(db.Text, nullable=False)
    """pem_data (str): PEM Encoded Certificate Data"""

    rsa_private_key_id = db.Column(db.Integer, db.ForeignKey('rsa_private_keys.id'))
    """rsa_private_key_id (int): Foreign key reference to an RSAPrivateKey IF the private key was generated by us."""
    rsa_private_key = db.relationship(
        'RSAPrivateKey',
        backref='certificates',
    )

    x509_cn = db.Column(db.String(64), nullable=True)
    """x509_cn (str): X.509 Common Name"""
    x509_ou = db.Column(db.String(32))
    """x509_ou (str): X.509 Organizational Unit"""
    x509_o = db.Column(db.String(64))
    """x509_o (str): X.509 Organization"""
    x509_c = db.Column(db.String(2))
    """x509_c (str): X.509 2 letter Country Code"""
    x509_st = db.Column(db.String(128))
    """x509_st (str): X.509 State or Location"""
    not_before = db.Column(db.DateTime(timezone=False), nullable=False)
    """not_before (datetime): Certificate validity - not before"""
    not_after = db.Column(db.DateTime(timezone=False), nullable=False)
    """not_after (datetime): Certificate validity - not after"""
    serial = db.Column(db.BigInteger)
    """serial (int): Serial Number"""
    # SHA-256 hash of DER-encoded certificate
    fingerprint = db.Column(db.String(64), nullable=False, index=True, unique=True)  # Unique
    """fingerprint (str): SHA-256 hash of certificate"""
    push_topic = db.Column(db.String, nullable=True)  # Only required for push certificate
    """push_topic (str): Only present for Push Certificates, the x.509 User ID field value"""
    discriminator = db.Column(db.String(20))
    """discriminator (str): The type of certificate"""

    __mapper_args__ = {
        'polymorphic_on': discriminator,
        'polymorphic_identity': 'certificates',
    }

    @classmethod
    def from_crypto_type(cls, certificate: x509.Certificate, certtype: CertificateType):
        # type: (certtype, x509.Certificate, CertificateType) -> Certificate
        m = cls()
        m.pem_data = certificate.public_bytes(serialization.Encoding.PEM)
        m.not_after = certificate.not_valid_after
        m.not_before = certificate.not_valid_before
        m.fingerprint = certificate.fingerprint(hashes.SHA256())
        m.discriminator = certtype.value
        m.serial = certificate.serial_number

        subject: x509.Name = certificate.subject
        cns = subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cns is not None:
            m.x509_cn = cns[0].value

        return m


class RSAPrivateKey(db.Model):
    """RSA Private Key Model"""
    __tablename__ = 'rsa_private_keys'

    #: id db.Column
    id = db.Column(db.Integer, primary_key=True)
    pem_data = db.Column(db.Text, nullable=False)

    @classmethod
    def from_crypto(cls, private_key: rsa.RSAPrivateKeyWithSerialization):
        """Convert a cryptography RSAPrivateKey object to an SQLAlchemy model."""
        # type: (type, rsa.RSAPrivateKeyWithSerialization) -> RSAPrivateKey
        m = cls()
        m.pem_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return m

    def to_crypto(self) -> rsa.RSAPrivateKey:
        """Convert an SQLAlchemy RSAPrivateKey model to a cryptography RSA Private Key."""
        pk = serialization.load_pem_private_key(
            self.pem_data,
            backend=default_backend(),
            password=None,
        )
        return pk


class CertificateSigningRequest(Certificate):
    """Polymorphic single table inheritance specifically for Certificate Signing Requests."""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.CSR.value
    }

    @classmethod
    def from_crypto(cls, csr: x509.CertificateSigningRequest):
        # type: (type, x509.CertificateSigningRequest, CertificateType) -> Certificate
        m = cls()
        m.pem_data = csr.public_bytes(serialization.Encoding.PEM)
        m.not_before = datetime.datetime.utcnow()
        m.not_after = datetime.datetime.utcnow() + datetime.timedelta(days=700)
        h = hashes.Hash(hashes.SHA256(), default_backend())
        h.update(m.pem_data)
        m.fingerprint = h.finalize()

        m.discriminator = CertificateType.CSR.value

        subject: x509.Name = csr.subject
        cns = subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cns is not None:
            m.x509_cn = cns[0].value

        return m


class SSLCertificate(Certificate):
    """Polymorphic single table inheritance specifically for SSL certificates assigned to the MDM for HTTPS traffic."""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.WEB.value
    }


class PushCertificate(Certificate):
    """Polymorphic single table inheritance specifically for APNS MDM Push Certificates assigned to the MDM."""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.PUSH.value
    }

    @classmethod
    def from_crypto(cls, certificate: x509.Certificate):
        m = Certificate.from_crypto_type(certificate, CertificateType.PUSH)
        return m


class CACertificate(Certificate):
    """Polymorphic single table inheritance specifically for Certificate Authorities generated by this MDM."""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.CA.value
    }

    @classmethod
    def from_crypto(cls, certificate: x509.Certificate):  # type: () -> CACertificate
        m = cls.from_crypto_type(certificate, CertificateType.CA)
        return m


class DeviceIdentityCertificate(Certificate):
    """Polymorphic single table inheritance specifically for device identity certificates."""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.DEVICE.value
    }

    @classmethod
    def from_crypto(cls, certificate: x509.Certificate):
        m = cls()
        m.pem_data = certificate.public_bytes(encoding=serialization.Encoding.PEM)
        m.not_after = certificate.not_valid_after
        m.not_before = certificate.not_valid_before
        m.fingerprint = certificate.fingerprint(hashes.SHA256())

        subject: x509.Name = certificate.subject

        cns = subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cns is not None:
            m.x509_cn = cns[0].value

        # m.x509_c = subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)
        # m.x509_o = subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
        # m.x509_ou = subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)
        # m.x509_st = subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)

        return m


class EncryptionCertificate(Certificate):
    """Polymorphic single table inheritance specifically for Encryption Certificates"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.ENCRYPT.value
    }

    @classmethod
    def from_crypto(cls, certificate: x509.Certificate):
        # TODO: sometimes serial numbers are too large even for SQLite BIGINT
        m = cls()
        m.pem_data = certificate.public_bytes(encoding=serialization.Encoding.PEM)
        m.not_after = certificate.not_valid_after
        m.not_before = certificate.not_valid_before
        m.fingerprint = certificate.fingerprint(hashes.SHA256())

        subject: x509.Name = certificate.subject

        cns = subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cns is not None:
            m.x509_cn = cns[0].value
        return m