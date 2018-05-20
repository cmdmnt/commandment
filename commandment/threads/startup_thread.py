"""
This thread should run delayed, once at startup to initialise the internal CA and self-signed certificates to provide
a baseline configuration for messing around with.
"""

import threading
import logging
import datetime
import os
from oscrypto.keys import parse_pkcs12
from commandment.models import db, CACertificate, CertificateSigningRequest, RSAPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import sqlalchemy
from flask import Flask

startup_thread = None
startup_delay = 5.0

logger = logging.getLogger(__name__)


def generate_ca(app: Flask):
    """Generate internal CA certificate for sandbox setups."""
    with app.app_context():
        try:
            ca_certificate = db.session.query(CACertificate).filter_by(x509_cn='COMMANDMENT-CA').one()
            logger.debug("COMMANDMENT-CA already generated")

        except sqlalchemy.orm.exc.MultipleResultsFound:
            logger.error("Multiple COMMANDMENT-CA Certificates were found, this should never happen.")

        except sqlalchemy.orm.exc.NoResultFound:
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


def split_pkcs12(app: Flask):
    """Split up .p12 containers if necessary."""
    with app.app_context():
        push_certificate_path = app.config['PUSH_CERTIFICATE']
        if not os.path.exists(push_certificate_path):
            raise RuntimeError('You specified a push certificate at: {}, but it does not exist.'.format(push_certificate_path))

        # We can handle loading PKCS#12 but APNS2Client specifically requests PEM encoded certificates
        push_certificate_basename, ext = os.path.splitext(push_certificate_path)
        if ext.lower() == '.p12':
            pem_key_path = push_certificate_basename + '.key'
            pem_certificate_path = push_certificate_basename + '.crt'

            if not os.path.exists(pem_key_path) or not os.path.exists(pem_certificate_path):
                app.logger.info('You provided a PKCS#12 push certificate, we will have to encode it as PEM to continue...')
                app.logger.info('.key and .crt files will be saved in the same location')

                with open(push_certificate_path, 'rb') as fd:
                    if 'PUSH_CERTIFICATE_PASSWORD' in app.config:
                        key, certificate, intermediates = parse_pkcs12(fd.read(), bytes(app.config['PUSH_CERTIFICATE_PASSWORD'], 'utf8'))
                    else:
                        key, certificate, intermediates = parse_pkcs12(fd.read())

                crypto_key = serialization.load_der_private_key(key.dump(), None, default_backend())
                with open(pem_key_path, 'wb') as fd:
                    fd.write(crypto_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()))

                crypto_cert = x509.load_der_x509_certificate(certificate.dump(), default_backend())
                with open(pem_certificate_path, 'wb') as fd:
                    fd.write(crypto_cert.public_bytes(serialization.Encoding.PEM))


def startup_callback(app: Flask):
    """Run the StartUp Thread jobs"""
    logger.debug("Started Thread: Startup")
    generate_ca(app)


def start(app: Flask):
    """Start the StartUp thread"""
    startup_thread = threading.Timer(startup_delay, startup_callback, [app])
    startup_thread.daemon = True
    startup_thread.start()
