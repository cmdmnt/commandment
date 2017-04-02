"""
These PKI models are a wrapper around the database model which separates the concerns of parsing and generating from
database operations. In this way the storage is not bound to the implementation.
"""

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from asn1crypto import pkcs12
from cryptography.hazmat.primitives import serialization, hashes
import werkzeug
import datetime
import commandment.models as dbmodels


class RSAPrivateKey(object):
    """RSAPrivateKey wraps the cryptography primitive and provides utility methods for encoding and decoding private
    keys."""

    def __init__(self, model: dbmodels.RSAPrivateKey = None, pk: rsa.RSAPrivateKey = None, password: str = None):
        if pk is not None:
            self._key = pk
        elif model is not None:
            self._model = model
            if self._model.pem_data is not None:
                self._key = serialization.load_pem_private_key(
                    self._model.pem_data,
                    password=password,
                    backend=default_backend()
                )

    @classmethod
    def generate(cls, key_size: int=2048):
        """Create an RSA private key.

        Args:
            key_size: RSA key size as an integer, default is 2048.

        Returns:
             cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey: The private key
        """
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )

        return cls(pk=key)

    @property
    def pem_key(self):
        """Get the private key with PEM encoding."""
        pem = self._key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem


class CertificateSigningRequest(object):

    @classmethod
    def generate(cls, name: x509.Name, key: RSAPrivateKey = None):
        """Create a Certificate Signing Request.

        If the private key is not supplied to this method then a new one will be generated and returned with the
        result. Otherwise, the supplied key is returned.

        Args:
            name: x509.Name to use in the request
            key: (optional) instance of RSAPrivateKey to use to generate the CSR

        Returns:
              Tuple of (private key, csr)
        """
        if key is None:
            key = RSAPrivateKey.generate()

        csr = x509.CertificateSigningRequestBuilder().subject_name(name).sign(key, hashes.SHA256(), default_backend())

        return key, csr

    def __init__(self, model: dbmodels.CertificateSigningRequest = None, csr: x509.CertificateSigningRequest = None):
        if csr is not None:
            self._csr = csr
        elif model is not None:
            self._model = model
            self.pem_data = model.pem_request

    @property
    def pem_data(self):
        if self._csr is None:
            return None

        return self._csr.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @pem_data.setter
    def pem_data(self, pem_data: bytes):
        self._csr = x509.load_pem_x509_csr(pem_data, default_backend())



class Certificate(object):

    def __init__(self, type: str, model: dbmodels.Certificate = None, certificate: x509.Certificate = None):
        if certificate is not None:
            self._certificate = certificate
            self._type = type
            self._model = None
            
        elif model is not None:
            self._model = model
            self._certificate = None
            self.pem_data = model.pem_data

    @property
    def pem_data(self):
        if self._certificate is not None:
            return self._certificate.public_bytes(
                serialization.Encoding.PEM
            )
        else:
            return self._model.pem_data

    @pem_data.setter
    def pem_data(self, pem_data: bytes):
        self._certificate = x509.load_pem_x509_certificate(pem_data, default_backend())

    @property
    def topic(self) -> str:
        subject = self._certificate.subject
        user_id = subject.get_attributes_for_oid(NameOID.USER_ID)
        return user_id.value

    @property
    def common_name(self) -> str:
        cn = self._certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return cn.value

    def model(self):
        if self._model is not None:
            return self._model
        else:
            if self._type == 'mdm.cacert':
                c = dbmodels.CACertificate()
            elif self._type == 'mdm.webcrt':
                c = dbmodels.SSLCertificate()
            elif self._type == 'mdm.pushcert':
                c = dbmodels.PushCertificate()
            else:
                raise ValueError('no suitable cert model available')

            c.pem_data = self.pem_data
            c.fingerprint = self._certificate.fingerprint(hashes.SHA256())
            c.not_after = self._certificate.not_valid_after
            c.not_before = self._certificate.not_valid_before
            
            subject = self._certificate.subject
            cn = subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            if cn is not None:
                c.x509_cn = cn[0].value

            return c


def certificate_from_pem_upload(file: werkzeug.datastructures.FileStorage) -> x509.Certificate:
    """Generate an instance of Certificate from an uploaded file."""
    return x509.load_pem_x509_certificate(file.read(), backend=default_backend())


def validate_pem_upload(file: werkzeug.datastructures.FileStorage):
    """Validate an uploaded certificate in PEM encoding"""
    cert = x509.load_pem_x509_certificate(file.read(), backend=default_backend())
    assert datetime.datetime.utcnow() > cert.not_valid_before
    assert datetime.datetime.utcnow() < cert.not_valid_after
    


