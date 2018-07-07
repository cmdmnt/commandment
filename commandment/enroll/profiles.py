import os.path
from typing import Optional
from uuid import uuid4
from flask import abort, current_app, url_for
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from commandment.profiles.certificates import KeyUsage
from commandment.profiles.models import SCEPPayload, PEMCertificatePayload, PKCS12CertificatePayload
from commandment.models import db, Organization, SCEPConfig
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from commandment.pki.openssl import create_pkcs12


def scep_payload_from_configuration() -> SCEPPayload:
    """Generate a SCEP Payload based upon the commandment system configuration.

    Returns:
        SCEPPayload: The created payload based upon current configuration.
    """
    # try:
    #     org = db.session.query(Organization).one()
    # except NoResultFound:
    #     abort(500, 'No organization is configured, cannot generate enrollment profile.')
    # except MultipleResultsFound:
    #     abort(500, 'Multiple organizations, backup your database and start again')

    try:
        scep_config = db.session.query(SCEPConfig).one()

        scep_payload = SCEPPayload(
            uuid=uuid4(),
            identifier='com.github.cmdmnt.commandment.scep',
            url=scep_config.url,
            name='',
            subject=[['CN', '%HardwareUUID%']],
            challenge=scep_config.challenge,
            key_size=scep_config.key_size,
            key_type='RSA',
            key_usage=scep_config.key_usage,
            display_name='Commandment SCEP Enroll Payload',
            description='Requests a certificate to identify your device to commandment',
            retries=scep_config.retries,
            retry_delay=scep_config.retry_delay,
            version=1
        )
    except NoResultFound:
        scep_payload = SCEPPayload(
            uuid=uuid4(),
            identifier='com.github.cmdmnt.commandment.scep',
            url=url_for('scep_app.scep'),
            name='',
            subject=[['CN', '%HardwareUUID%']],
            challenge=current_app.config.get('SCEPY_CHALLENGE', None),
            key_size=2048,
            key_type='RSA',
            key_usage=KeyUsage.All,
            display_name='Commandment SCEP Enroll Payload',
            description='Requests a certificate to identify your device to commandment',
            retries=3,
            retry_delay=10,
            version=1
        )
    except MultipleResultsFound:
        return abort(500, 'Multiple SCEP configs, this should never happen.')

    return scep_payload


def ca_trust_payload_from_configuration() -> PEMCertificatePayload:
    """Create a CA payload with the PEM representation of the Certificate Authority used by this instance.

    You need to check whether the app config contains 'CA_CERTIFICATE' before invoking this.
    """
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    with open(current_app.config['CA_CERTIFICATE'], 'rb') as fd:
        pem_data = fd.read()
        pem_payload = PEMCertificatePayload(
            uuid=uuid4(),
            identifier=org.payload_prefix + '.ca',
            payload_content=pem_data,
            display_name='Certificate Authority',
            description='Required for your device to trust the server',
            type='com.apple.security.root',
            version=1
        )

        return pem_payload


def ssl_trust_payload_from_configuration() -> PEMCertificatePayload:
    """Generate a PEM certificate payload in order to trust this host.

    """
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    basepath = os.path.dirname(__file__)
    certpath = os.path.join(basepath, current_app.config['SSL_CERTIFICATE'])

    with open(certpath, 'rb') as fd:
        pem_payload = PEMCertificatePayload(
            uuid=uuid4(),
            identifier=org.payload_prefix + '.ssl',
            payload_content=fd.read(),
            display_name='Web Server Certificate',
            description='Required for your device to trust the server',
            type='com.apple.security.pkcs1',
            version=1
        )
        return pem_payload


def identity_payload(private_key: rsa.RSAPrivateKeyWithSerialization,
                     certificate: x509.Certificate,
                     passphrase: Optional[str] = None) -> PKCS12CertificatePayload:
    """Generate a PKCS#12 certificate payload for device identity."""
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    pkcs12_data = create_pkcs12(private_key, certificate, passphrase)

    pkcs12_payload = PKCS12CertificatePayload(
        uuid=uuid4(),
        certificate_file_name='device_identity.p12',
        identifier=org.payload_prefix + '.identity',
        display_name='Device Identity Certificate',
        description='Required to identify your device to the MDM',
        type='com.apple.security.pkcs12',
        password=passphrase,
        payload_content=pkcs12_data,
        version=1
    )

    return pkcs12_payload
