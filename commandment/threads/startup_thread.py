"""
This thread should run delayed, once at startup to initialise the internal CA and self-signed certificates to provide
a baseline configuration for messing around with.
"""

import threading
import logging
import datetime
import os
from flask_alembic import Alembic
from oscrypto.keys import parse_pkcs12
from commandment.models import db
from commandment.pki.models import RSAPrivateKey, CertificateSigningRequest, CACertificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import sqlalchemy
from commandment.pki.ca import get_ca
from flask import Flask

startup_thread = None
startup_delay = 1.0

logger = logging.getLogger('startup thread')


def generate_ca(app: Flask):
    """Generate internal CA certificate for sandbox setups."""
    with app.app_context():
        app.logger.info('Generating Internal CA if necessary...')
        ca = get_ca()  # Implicit creation of `certificate_authority` row and certificates


def split_pkcs12(app: Flask):
    """Split up .p12 containers if necessary."""
    with app.app_context():
        if 'PUSH_CERTIFICATE' not in app.config:
            app.logger.warn('No push certificate specified, you will not be able to manage devices until this is configured')
            return

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
                app.logger.info('.key and .crt files will be saved in the same location: %s, %s', pem_key_path, pem_certificate_path)
                with open(push_certificate_path, 'rb') as fd:
                    if 'PUSH_CERTIFICATE_PASSWORD' in app.config:
                        key, certificate, intermediates = parse_pkcs12(fd.read(), bytes(app.config['PUSH_CERTIFICATE_PASSWORD'], 'utf8'))
                    else:
                        key, certificate, intermediates = parse_pkcs12(fd.read())

                try:
                    crypto_key = serialization.load_der_private_key(key.dump(), None, default_backend())
                    with open(pem_key_path, 'wb') as fd:
                        fd.write(crypto_key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.NoEncryption()))

                    crypto_cert = x509.load_der_x509_certificate(certificate.dump(), default_backend())
                    with open(pem_certificate_path, 'wb') as fd:
                        fd.write(crypto_cert.public_bytes(serialization.Encoding.PEM))
                except PermissionError:
                    app.logger.error('Could not write out .key or .crt file. You will not be able to push APNS messages')
                    app.logger.error('This means your MDM is BROKEN until you fix permissions')
            else:
                app.logger.info('.p12 already split into PEM/KEY components')


def run_migrations(app: Flask):
    """Run the database migrations."""
    with app.app_context():
        app.logger.info('Running Alembic Migrations')
        alembic = Alembic()
        alembic.init_app(app, run_mkdir=False)
        alembic.upgrade('head')


def startup_callback(app: Flask):
    """Run the StartUp Thread jobs"""
    logger.debug("Started Thread: Startup")
    split_pkcs12(app)
    run_migrations(app)
    generate_ca(app)


def start(app: Flask):
    """Start the StartUp thread"""
    logger.info('Startup thread will run in 5 seconds')
    startup_thread = threading.Timer(startup_delay, startup_callback, [app])
    startup_thread.daemon = True
    startup_thread.start()
