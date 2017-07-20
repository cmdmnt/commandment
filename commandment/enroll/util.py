import os.path
from flask import abort, current_app
from commandment.models import db, Organization, SCEPConfig
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.name import NameOID
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from commandment.profiles import PayloadScope
from commandment.profiles.models import Profile, PEMCertificatePayload, SCEPPayload, MDMPayload
from uuid import uuid4


def generate_enroll_profile() -> Profile:
    """Generate an enrollment profile.

    If the user specified a CA certificate, we assume that it won't be trusted by default, so it is included in the
    enrollment profile.

    If the user specified an SSL certificate, we assume that it won't be trusted by default.

    You need to have an organization configured to generate organization information in the profile, and to establish
    the payload prefix.

    """
    try:
        org = db.session.query(Organization).one()
    except NoResultFound:
        abort(500, 'No organization is configured, cannot generate enrollment profile.')
    except MultipleResultsFound:
        abort(500, 'Multiple organizations, backup your database and start again')

    push_certificate_path = os.path.join(os.path.dirname(current_app.root_path), current_app.config['PUSH_CERTIFICATE'])

    try:
        scep_config = db.session.query(SCEPConfig).one()
    except NoResultFound:
        abort(500, 'No SCEP Configuration found, cannot generate enrollment profile.')

    if os.path.exists(push_certificate_path):
        push_certificate_basename, ext = os.path.splitext(push_certificate_path)
        if ext.lower() == '.p12':  # push service will have re-exported the PKCS#12 container
            push_certificate_path = push_certificate_basename + '.crt'

        with open(push_certificate_path, 'rb') as fd:
            push_certificate = x509.load_pem_x509_certificate(fd.read(), backend=default_backend())
    else:
        abort(500, 'No push certificate available at: {}'.format(push_certificate_path))

    if not org:
        abort(500, 'No MDM configuration present; cannot generate enrollment profile')

    if not org.payload_prefix:
        abort(500, 'MDM configuration has no profile prefix')

    profile = Profile(
        identifier=org.payload_prefix + '.enroll',
        uuid=uuid4(),
        display_name='Commandment Enrollment Profile',
        description='Enrolls your device for Mobile Device Management',
        organization=org.name,
        version=1,
        scope=PayloadScope.System,
    )

    if 'CA_CERTIFICATE' in current_app.config:
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
            profile.payloads.append(pem_payload)

    # Include Self Signed Certificate if necessary
    # TODO: Check that cert is self signed.
    if 'SSL_CERTIFICATE' in current_app.config:
        basepath = os.path.dirname(__file__)
        certpath = os.path.join(basepath, current_app.config['SSL_CERTIFICATE'])
        with open(certpath, 'rb') as fd:
            # ssl_certificate = x509.load_pem_x509_certificate(fd.read(), backend=default_backend())
            # der_payload = PEMCertificatePayload(
            #     uuid=uuid4(),
            #     identifier=org.payload_prefix + '.ssl',
            #     payload_content=ssl_certificate.public_bytes(serialization.Encoding.DER),
            #     display_name='Web Server Certificate',
            #     description='Required for your device to trust the server',
            #     type='com.apple.security.pem',
            # )
            # profile.payloads.append(der_payload)
            pem_payload = PEMCertificatePayload(
                uuid=uuid4(),
                identifier=org.payload_prefix + '.ssl',
                payload_content=fd.read(),
                display_name='Web Server Certificate',
                description='Required for your device to trust the server',
                type='com.apple.security.pkcs1',
                version=1
            )
            profile.payloads.append(pem_payload)

    scep_payload = SCEPPayload(
        uuid=uuid4(),
        identifier=org.payload_prefix + '.mdm-scep',
        url=scep_config.url,
        name='MDM SCEP',
        subject=[['CN', '%HardwareUUID%']],
        challenge=scep_config.challenge,
        key_size=scep_config.key_size,
        key_type='RSA',
        key_usage=scep_config.key_usage,
        display_name='MDM SCEP',
        description='Requests a certificate to identify your device',
        retries=scep_config.retries,
        retry_delay=scep_config.retry_delay,
        version=1
    )

    profile.payloads.append(scep_payload)
    cert_uuid = scep_payload.uuid

    from commandment.mdm import AccessRights

    push_topics = push_certificate.subject.get_attributes_for_oid(NameOID.USER_ID)
    if len(push_topics) != 1:
        abort(500, 'Unexpected missing or invalid push topic in Push Certificate')

    push_topic = push_topics[0].value

    mdm_payload = MDMPayload(
        uuid=uuid4(),
        identifier=org.payload_prefix + '.mdm',
        identity_certificate_uuid=cert_uuid,
        topic=push_topic,
        server_url='https://{}:{}/mdm'.format(current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']),
        access_rights=AccessRights.All.value,
        check_in_url='https://{}:{}/checkin'.format(current_app.config['PUBLIC_HOSTNAME'], current_app.config['PORT']),
        sign_message=True,
        check_out_when_removed=True,
        display_name='Device Configuration and Management',
        server_capabilities=['com.apple.mdm.per-user-connections'],
        description='Enrolls your device with the MDM server',
        version=1
    )
    profile.payloads.append(mdm_payload)

    return profile
