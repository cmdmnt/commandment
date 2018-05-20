"""
This thread should run delayed, once at startup to initialise the internal CA and self-signed certificates to provide
a baseline configuration for messing around with.
"""

import threading
import logging
import datetime
from commandment.models import db, CACertificate, CertificateSigningRequest, RSAPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID

startup_thread = None
startup_delay = 5.0

logger = logging.getLogger(__name__)


def startup_callback():
    """Run the StartUp Thread jobs"""
    logger.debug("Started Thread: Startup")

    logger.debug("Generating Private Key for COMMANDMENT-CA")
    # Create CA Certificate if not Available to bootstrap internal CA
    # Issue a Certificate to receive encrypted replies from mdmcert.download
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    key_model = RSAPrivateKey.from_crypto(key)
    db.session.add(key_model)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "COMMANDMENT-CA"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Commandment")
    ])

    logger.debug("Generating CA Certificate for COMMANDMENT-CA")
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=900)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    ).sign(key, hashes.SHA256(), default_backend())

    cert_model = CACertificate.from_crypto(cert)
    db.session.add(cert_model)

    db.session.commit()


def start():
    """Start the StartUp thread"""
    startup_thread = threading.Timer(startup_delay, startup_callback, None)
    startup_thread.daemon = True
    startup_thread.start()
