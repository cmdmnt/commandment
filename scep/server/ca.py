"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from typing import Type
from flask import g, current_app
import os
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from asn1crypto.cms import SignerIdentifier, IssuerAndSerialNumber
from oscrypto.asymmetric import load_certificate, load_private_key, generate_pair, Certificate

STORAGE_DIRS = [
    'certs',
    'crl',
    'newcerts',
    'private'
]


class CertificateAuthority(object):
    """The CertificateAuthority Class implements a basic Cert Authority.
    
    It is recommended to use an external CA if possible.
    """

    default_subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'COMMANDMENT-SCEP-CA'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'commandment'),
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'US')
    ])

    @classmethod
    def load_or_create(cls, path: str, subject: x509.Name = default_subject, key_size: int = 2048):
        """Load or create a certificate authority at path

        Generates a new private key and self-signs a CA certificate.

        Args:
            path (str): The base path where the CA will be stored.
            subject (cryptography.x509.Name): The subject of the CA
            key_size (int): The RSA private key size integer, default is 2048.

        Returns:
            Instance of CertificateAuthority
        """
        key_path = os.path.join(path, 'private', 'ca.key.pem')
        cert_path = os.path.join(path, 'certs', 'ca.cer')

        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    data=key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        else:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend(),
            )

        if os.path.exists(cert_path):
            with open(cert_path, 'rb') as cert_file:
                certificate = x509.load_der_x509_certificate(
                    data=cert_file.read(),
                    backend=default_backend()
                )
        else:
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
            ).add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    content_commitment=False,
                    key_encipherment=True,
                    data_encipherment=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False
                ),
                True
            ).sign(private_key, hashes.SHA256(), default_backend())

        ca = cls(path, certificate, private_key)
        return ca

    def __init__(self, path: str, certificate: x509.Certificate, private_key: rsa.RSAPrivateKeyWithSerialization, password=None):
        """
        Args:
            path: Storage path
            certificate: Instance of commandment.pki.models.Certificate with the BasicConstraints CA extension
            private_key: Instance of commandment.pki.models.RSAPrivateKey
            password: Private key password if required (Ignored currently)
            
        """
        self._path = path
        self._certificate = certificate
        self._private_key = private_key
        self._persist_ca(self._certificate, self._private_key, password)

    @property
    def path(self):
        return self._path

    @property
    def certificate(self) -> x509.Certificate:
        """Retrieve the CA Certificate"""
        return self._certificate

    @property
    def private_key(self) -> rsa.RSAPrivateKey:
        """Retrieve the CA Private Key"""
        return self._private_key

    def _persist_ca(self, certificate: x509.Certificate, private_key: rsa.RSAPrivateKeyWithSerialization, password=None):
        """Persist the CA key pair to storage."""
        with open(os.path.join(self._path, 'certs', 'ca.cer'), 'wb') as fd:
            cert_bytes = certificate.public_bytes(serialization.Encoding.DER)
            fd.write(cert_bytes)

        with open(os.path.join(self._path, 'private', 'ca.key.pem'), 'wb') as fd:
            if password:
                enc = serialization.BestAvailableEncryption(password)
            else:
                enc = serialization.NoEncryption()

            key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=enc
            )
            fd.write(key_bytes)

    def signer_identifier(self) -> SignerIdentifier:
        """Get the identity of this CA instance as a SignerIdentifier structure for CMS."""
        ias = IssuerAndSerialNumber()
        #ias['issuer'] = self.certificate.issuer  # probably wont work, need to get the asn1crypto type
        ias['serial_number'] = self.certificate.serial_number
        sid = SignerIdentifier('issuer_and_serial_number', ias)

        return sid

    def sign(self, csr: x509.CertificateSigningRequest) -> x509.Certificate:
        """Sign a certificate signing request.

        Args:
            csr (x509.CertificateSigningRequest): The certificate signing request
        Returns:
            Instance of x509.Certificate
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


def ca_from_storage(path: str) -> CertificateAuthority:
    """Create a new CertificateAuthority at the given path."""
    if not os.path.exists(path):
        os.mkdir(path)

    for d in STORAGE_DIRS:
        abspath = os.path.join(path, d)
        if not os.path.exists(abspath):
            os.mkdir(abspath)

    ca = CertificateAuthority.load_or_create(path)
    return ca


def get_ca() -> CertificateAuthority:
    ca = getattr(g, '_mdm_ca', None)
    if ca is None:
        ca = g._mdm_ca = ca_from_storage(current_app.config['CA_ROOT'])
    return ca
