'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''Commandment MDM Certificate Authority'''

from flask import g, current_app
from ..database import db_session, NoResultFound
from ..models import (Certificate as DBCertificate,
                      PrivateKey as DBPrivateKey,
                      InternalCA)
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


MDM_CA_CN = 'MDM CA'
MDM_DEVICE_CN = 'MDM Device'


def from_database_or_create():
    """Create a new CertificateAuthority from the keypair in the database, or generate new ones if they do not exist.

    :returns: A new (or existing) certificate authority
    :rtype: CertificateAuthority
    """
    try:
        db_cert, db_pk = db_session.query(DBCertificate, DBPrivateKey) \
            .join(DBCertificate, DBPrivateKey.certificates) \
            .filter(DBCertificate.cert_type == 'mdm.cacert') \
            .one()
        private_key, cert = db_pk.to_crypto(), db_cert.to_crypto()
        ca = CertificateAuthority(cert, private_key)

    except NoResultFound:
        ca = CertificateAuthority.create()

        db_cert = DBCertificate.from_crypto(ca.certificate, 'mdm.cacert')
        db_pk = DBPrivateKey.from_crypto(ca.private_key)

        db_pk.certificates.append(db_cert)

        db_session.add(db_cert)
        db_session.add(db_pk)

        db_session.commit()

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
        x509.NameAttribute(NameOID.COMMON_NAME, u'commandment.dev'),
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
            x509.BasicConstraints(True, None)
        ).sign(private_key, hashes.SHA256(), default_backend())

        ca = cls(certificate, private_key)
        return ca

    def __init__(self, certificate: x509.Certificate, private_key: rsa.RSAPrivateKey, password=None):
        """
        Args:
            certificate: Instance of cryptography.x509.Certificate with the BasicConstraints CA extension
            private_key: Instance of cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
            password: Private key password if required (Ignored currently)
            
        """
        self._certificate = certificate
        self._private_key = private_key

    @property
    def certificate(self) -> x509.Certificate:
        return self._certificate

    @certificate.setter
    def certificate(self, value):
        if isinstance(value, str):  # we will assume a PEM string
            cert = x509.load_pem_x509_certificate(value, default_backend())
            self._certificate = cert
        elif isinstance(value, x509.Certificate):
            self._certificate = value
        else:
            raise ValueError('Supplied invalid value for CA certificate')

    @property
    def pem_certificate(self) -> str:
        """Retrieve the CA certificate as a PEM encoded cert."""
        serialized = self._certificate.public_bytes(
            encoding=serialization.Encoding.PEM
        )
        return serialized

    @property
    def private_key(self) -> rsa.RSAPrivateKey:
        return self._private_key

    def export_ca_certificate(self, format='pem'):
        """Export the CA certificate.

        :param str format: The format, 'pem' or 'der'
        :returns: Certificate data
        :rtype: Buffer
        """
        pass
        # if format == 'pem':
        #     return self.certificate.public_bytes(
        #         serialization.Encoding.PEM
        #     )
        # else:
        #     raise ValueError('Unsupported export format')

    def sign(self, csr: x509.CertificateSigningRequest) -> x509.Certificate:
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



        # def sign_new_device_req(self, csr):
        #     '''Sign and persist a new device certificate request'''
        #     signed = self.sign(csr)
        #     #db_dev_crt = self.save_new_device_cert(dev_signed_cert)
        #
        #     #return dev_signed_cert, db_dev_crt
        #
        # def save_new_device_cert(self, cert):
        #     # cert should be of type Certificate
        #     db_dev_crt = DBCertificate.from_x509(cert, 'mdm.device')
        #     db_session.add(db_dev_crt)
        #     db_session.commit()
        #
        #     return db_dev_crt
        #
        # def gen_new_device_identity(self):
        #     # we don't persist the key as it should only be held and used by
        #     # the client device
        #     dev_csr, dev_key = CertificateRequest.with_new_private_key(CN=MDM_DEVICE_CN)
        #
        #     dev_crt, db_dev_crt = self.sign_new_device_req(dev_csr)
        #
        #     return (Identity(dev_key, dev_crt), db_dev_crt)



def get_or_generate_web_certificate(cn: str) -> (str, str, str):
    mdm_ca = get_ca()
    try:
        q = db_session.query(DBCertificate, DBPrivateKey) \
            .join(DBCertificate, DBPrivateKey.certificates) \
            .filter(DBCertificate.cert_type == 'mdm.webcrt')
        result = q.first()
        if not result:
            q.one()
        else:
            db_cert, db_pk = result
        # TODO: return chain!
        return (db_cert.pem_certificate, db_pk.pem_key, mdm_ca.export_ca_certificate())
    except NoResultFound:
        web_pk = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        web_req = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'commandment.dev')
        ])).sign(web_pk, hashes.SHA256(), default_backend())

        web_crt = mdm_ca.sign(web_req)

        db_cert = DBCertificate.from_crypto(web_crt, 'mdm.webcrt')
        db_pk = DBPrivateKey.from_crypto(web_pk)

        db_session.add(db_cert)
        db_session.add(db_pk)

        db_pk.certificates.append(db_cert)

        db_session.commit()

        return (db_cert.pem_certificate, db_pk.pem_key, mdm_ca.export_ca_certificate())
