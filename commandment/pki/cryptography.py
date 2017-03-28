from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from asn1crypto import pkcs12
import werkzeug
import datetime


class Certificate(x509.Certificate):
    """The commandment Certificate class wraps cryptography.x509.Certificate to provide some convenience accessors."""
    def __init__(self, *args, **kwargs):
        super(Certificate, self).__init__()

    @property
    def topic(self) -> str:
        subject = self.subject
        user_id = subject.get_attributes_for_oid(NameOID.USER_ID)
        return user_id.value

    @property
    def common_name(self) -> str:
        cn = self.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return cn.value


def certificate_from_pem_upload(file: werkzeug.datastructures.FileStorage) -> x509.Certificate:
    """Generate an instance of Certificate from an uploaded file."""
    return x509.load_pem_x509_certificate(file.read(), backend=default_backend())


def validate_pem_upload(file: werkzeug.datastructures.FileStorage):
    """Validate an uploaded certificate in PEM encoding"""
    cert = x509.load_pem_x509_certificate(file.read(), backend=default_backend())
    assert datetime.datetime.utcnow() > cert.not_valid_before
    assert datetime.datetime.utcnow() < cert.not_valid_after
    


