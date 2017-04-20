'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''Commandment MDM Certificate Authority'''

from flask import g, current_app
from ..models import db
from sqlalchemy.orm.exc import NoResultFound
import commandment.pki.models as models
import commandment.models as dbmodels
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


MDM_CA_CN = 'MDM CA'
MDM_DEVICE_CN = 'MDM Device'


def from_database_or_create():
    """Create a new CertificateAuthority from the keypair in the database,
    or generate new ones if they do not exist.

    Returns:
        A new (or existing) certificate authority.
    """
    try:
        db_cert = db.session.query(dbmodels.CACertificate).filter(dbmodels.CACertificate.discriminator == 'mdm.cacert').one()
        db_pk = db_cert.rsa_private_key
        private_key, cert = models.RSAPrivateKey(model=db_pk), models.Certificate('mdm.cacert', model=db_cert)
        ca = CertificateAuthority(cert, private_key)

    except NoResultFound:
        ca = CertificateAuthority.create()

        db_cert = ca.certificate.model()
        db_pk = dbmodels.RSAPrivateKey(pem_data=ca.private_key.pem_key)
        db_cert.rsa_private_key = db_pk
        
        db.session.add(db_cert)
        db.session.add(db_pk)

        db.session.commit()

    return ca


def get_ca():
    ca = getattr(g, '_mdm_ca', None)
    if ca is None:
        ca = g._mdm_ca = from_database_or_create()
    return ca


class CertificateAuthority(object):
    """The CertificateAuthority Class implements a basic Cert Authority.
    
    It is recommended to use an external CA if possible.
    """

    default_subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'COMMANDMENT-CA'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'commandment'),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, u'mosen@noreply.users.github.com'),
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'US')
    ])

    @classmethod
    def create(cls, subject=default_subject, key_size=2048):
        """Create a new Certificate Authority.

        Generates a new private key and self-signs a CA certificate.

        Args:
            subject: cryptography.x509.Name The certificate subject to use
            key_size: The RSA private key size integer, default is 2048.

        Returns:
            Instance of CertificateAuthority
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend(),
        )
        pk_model = models.RSAPrivateKey(pk=private_key)
        
        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            True
        ).sign(private_key, hashes.SHA256(), default_backend())
        cert_model = models.Certificate('mdm.cacert', certificate=certificate)

        ca = cls(cert_model, pk_model)
        return ca

    def __init__(self, certificate: models.Certificate, private_key: models.RSAPrivateKey, password=None):
        """
        Args:
            certificate: Instance of commandment.pki.models.Certificate with the BasicConstraints CA extension
            private_key: Instance of commandment.pki.models.RSAPrivateKey
            password: Private key password if required (Ignored currently)
            
        """
        self._certificate = certificate
        self._private_key = private_key

    @property
    def certificate(self) -> models.Certificate:
        """Retrieve the CA Certificate"""
        return self._certificate

    @property
    def private_key(self) -> models.RSAPrivateKey:
        """Retrieve the CA Private Key"""
        return self._private_key

    def generate(self, type: str, subject: x509.Name) -> (models.RSAPrivateKey, models.Certificate):
        """Generate a new private key and certificate with the given subject, and sign it with this CA.

        Args:
            type: Certificate type i.e `mdm.webcrt` or `mdm.cacert`
            subject: x509.Name the subject of the certificate being generated.
        Returns:
            (models.RSAPrivateKey, models.Certificate)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        pk_model = models.RSAPrivateKey(pk=private_key)

        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.certificate.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).sign(self.private_key.raw, hashes.SHA256(), default_backend())

        cert_model = models.Certificate(type=type, certificate=certificate)

        return pk_model, cert_model


    def sign(self, csr: models.CertificateSigningRequest) -> models.Certificate:
        """Sign a certificate signing request.

        :param CertificateSigningRequest csr: The signing request
        :returns: The signed certificate
        :rtype: x509.Certificate
        """
        builder = x509.CertificateBuilder()
        cert = builder.subject_name(
            csr.subject
        ).issuer_name(
            self.certificate.subject
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).serial_number(x509.random_serial_number()).public_key(
            csr.public_key()
        ).sign(self.private_key, hashes.SHA256(), default_backend())

        return cert


def get_or_generate_web_certificate(cn: str) -> (str, str, str):
    mdm_ca = get_ca()
    try:
        result = db.session.query(dbmodels.SSLCertificate).filter(dbmodels.SSLCertificate.discriminator == 'mdm.webcrt').one()

        # TODO: return chain!
        return (result.pem_data, result.rsa_private_key.pem_data, mdm_ca.certificate.pem_data)
    except NoResultFound:
        pk, cert = mdm_ca.generate('mdm.webcrt', x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'commandment')
        ]))

        db_pk = pk.model()
        db_cert = cert.model()
        db.session.add(db_cert)
        db.session.add(db_pk)

        db_cert.rsa_private_key = db_pk

        db.session.commit()

        return db_cert.pem_data, db_pk.pem_data, mdm_ca.certificate.pem_data
