import pytest
from commandment.threads import startup_thread
from commandment.pki.models import CACertificate


class TestStartupThread:

    def test_startup_thread_ca(self, session):
        """Assert that the startup thread actually creates self-signed certificates."""
        startup_thread.startup_callback()
        certificate = session.query(CACertificate).one()
        assert certificate.x509_cn == 'COMMANDMENT-CA'
        assert certificate.pem_data is not None
        assert certificate.fingerprint is not None
