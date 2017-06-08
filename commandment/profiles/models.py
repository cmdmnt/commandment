from enum import Enum

from sqlalchemy import Column, Integer, LargeBinary, String, Text, Enum as DBEnum, Boolean, ForeignKey, DateTime, \
    BigInteger

from commandment.profiles import PayloadScope
from commandment.profiles.certificates import KeyUsage
from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4

from ..models import db


class Payload(db.Model):
    __tablename__ = 'payloads'

    id = Column(Integer, primary_key=True)
    type = Column(String, index=True, nullable=False)
    version = Column(Integer, default=1)
    identifier = Column(String)
    uuid = Column(GUID, index=True, default=uuid4(), nullable=False)
    display_name = Column(String)
    description = Column(Text)
    organization = Column(String)

    # Dependencies should be tracked in cases where the payload refers to another required payload.
    # eg. a reference to certificate payload in an 802.1x configuration.
    # depends_on = relationship("Payload",
    #                           secondary=payload_dependencies,
    #                           backref="dependents")

    __mapper_args__ = {
        'polymorphic_identity': 'payload',
        'polymorphic_on': type,
    }


class MDMPayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    identity_certificate_uuid = Column(GUID, nullable=False)
    topic = Column(String, nullable=False)
    server_url = Column(String, nullable=False)
    server_capabilities = Column(String)
    sign_message = Column(Boolean)
    check_in_url = Column(String)
    check_out_when_removed = Column(Boolean)
    access_rights = Column(Integer)
    use_development_apns = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.mdm'
    }


class SCEPPayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, nullable=True)
    subject = Column(JSONEncodedDict, nullable=False)  # eg. O=x/OU=y/CN=z
    challenge = Column(String, nullable=True)
    key_size = Column(Integer, default=2048, nullable=False)
    ca_fingerprint = Column(LargeBinary, nullable=True)
    key_type = Column(String, default='RSA', nullable=False)
    key_usage = Column(DBEnum(KeyUsage), default=KeyUsage.All)
    subject_alt_name = Column(String, nullable=True)
    retries = Column(Integer, default=3, nullable=False)
    retry_delay = Column(Integer, default=10, nullable=False)
    certificate_renewal_time_interval = Column(Integer, default=14, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.scep',
    }


class CertificatePayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    certificate_file_name = Column(String)
    payload_content = Column(LargeBinary)
    password = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': 'certificate'
    }


class PEMCertificatePayload(CertificatePayload):
    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.pem'
    }


class DERCertificatePayload(CertificatePayload):
    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.pkcs1'
    }


class PKCS12CertificatePayload(CertificatePayload):
    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.pkcs12'
    }


profile_payloads = db.Table('profile_payloads', db.metadata,
                            Column('profile_id', Integer, ForeignKey('profiles.id')),
                            Column('payload_id', Integer, ForeignKey('payloads.id')))


profile_tags = db.Table('profile_tags', db.metadata,
                    db.Column('profile_id', Integer, ForeignKey('profiles.id')),
                    db.Column('tag_id', Integer, ForeignKey('tags.id')),
                    )


class Profile(db.Model):
    """Top level profile.

    See Also:
          - `Configuration Profile Keys
            <https://developer.apple.com/library/content/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html#//apple_ref/doc/uid/TP40010206-CH1-SW7>`_.

    Attributes:

    """
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)

    description = Column(Text)
    display_name = Column(String)
    expiration_date = Column(DateTime)  # Only for old style OTA
    identifier = Column(String, nullable=False)
    organization = Column(String)
    uuid = Column(GUID, index=True, default=uuid4())
    removal_disallowed = Column(Boolean)
    version = Column(Integer, default=1)
    payload_type = Column(String, default='Configuration')
    scope = Column(DBEnum(PayloadScope), default=PayloadScope.User.value)
    removal_date = Column(DateTime)
    duration_until_removal = Column(BigInteger)
    consent_en = Column(Text)
    is_encrypted = Column(Boolean, default=False)

    payloads = db.relationship('Payload',
                               secondary=profile_payloads,
                               backref='profiles')

    tags = db.relationship('Tag',
                           secondary=profile_tags,
                           backref='profiles')

