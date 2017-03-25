from cryptography import x509
from cryptography.x509.oid import NameOID


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
