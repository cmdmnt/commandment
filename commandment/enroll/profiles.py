import os.path
from uuid import uuid4
from flask import abort, current_app
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from commandment.profiles.models import SCEPPayload, PEMCertificatePayload
from commandment.models import db, Organization, SCEPConfig


def scep_payload_from_configuration() -> SCEPPayload:
    """Generate a SCEP Payload based upon the commandment system configuration.

    Returns:
        SCEPPayload: The created payload based upon current configuration.
    """
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    try:
        scep_config = db.session.query(SCEPConfig).one()
    except NoResultFound:
        abort(500, 'No SCEP Configuration found, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple SCEP configs, this should never happen.')

    scep_payload = SCEPPayload(
        uuid=uuid4(),
        identifier=org.payload_prefix + '.mdm-scep',
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
