from commandment.profiles import PayloadScope
from commandment.profiles.certificates import KeyUsage
from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4

from ..models import db


class Payload(db.Model):
    __tablename__ = 'payloads'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, index=True, nullable=False)
    version = db.Column(db.Integer, default=1)
    identifier = db.Column(db.String)
    uuid = db.Column(GUID, index=True, default=uuid4(), nullable=False)
    display_name = db.Column(db.String)
    description = db.Column(db.Text)
    organization = db.Column(db.String)

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
    id = db.Column(db.Integer, db.ForeignKey('payloads.id'), primary_key=True)
    identity_certificate_uuid = db.Column(GUID, nullable=False)
    topic = db.Column(db.String, nullable=False)
    server_url = db.Column(db.String, nullable=False)
    server_capabilities = db.Column(db.String)
    sign_message = db.Column(db.Boolean)
    check_in_url = db.Column(db.String)
    check_out_when_removed = db.Column(db.Boolean)
    access_rights = db.Column(db.Integer)
    use_development_apns = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.mdm'
    }


class SCEPPayload(Payload):
    id = db.Column(db.Integer, db.ForeignKey('payloads.id'), primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    subject = db.Column(JSONEncodedDict, nullable=False)  # eg. O=x/OU=y/CN=z
    challenge = db.Column(db.String, nullable=True)
    key_size = db.Column(db.Integer, default=2048, nullable=False)
    ca_fingerprint = db.Column(db.LargeBinary, nullable=True)
    key_type = db.Column(db.String, default='RSA', nullable=False)
    key_usage = db.Column(db.Enum(KeyUsage), default=KeyUsage.All)
    subject_alt_name = db.Column(db.String, nullable=True)
    retries = db.Column(db.Integer, default=3, nullable=False)
    retry_delay = db.Column(db.Integer, default=10, nullable=False)
    certificate_renewal_time_interval = db.Column(db.Integer, default=14, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.scep',
    }


class CertificatePayload(Payload):
    id = db.Column(db.Integer, db.ForeignKey('payloads.id'), primary_key=True)
    certificate_file_name = db.Column(db.String)
    payload_content = db.Column(db.LargeBinary)
    password = db.Column(db.String)
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
                            db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id')),
                            db.Column('payload_id', db.Integer, db.ForeignKey('payloads.id')))


profile_tags = db.Table('profile_tags', db.metadata,
                    db.Column('profile_id',  db.Integer, db.ForeignKey('profiles.id')),
                    db.Column('tag_id',  db.Integer, db.ForeignKey('tags.id')),
                    )


class Profile(db.Model):
    """Top level profile.

    See Also:
          - `Configuration Profile Keys
            <https://developer.apple.com/library/content/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html#//apple_ref/doc/uid/TP40010206-CH1-SW7>`_.

    Attributes:

    """
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

    description = db.Column(db.Text)
    display_name = db.Column(db.String)
    expiration_date = db.Column(db.DateTime)  # Only for old style OTA
    identifier = db.Column(db.String, nullable=False)
    organization = db.Column(db.String)
    uuid = db.Column(GUID, index=True, default=uuid4())
    removal_disallowed = db.Column(db.Boolean)
    version = db.Column(db.Integer, default=1)
    payload_type = db.Column(db.String, default='Configuration')
    scope = db.Column(db.Enum(PayloadScope), default=PayloadScope.User.value)
    removal_date = db.Column(db.DateTime)
    duration_until_removal = db.Column(db.BigInteger)
    consent_en = db.Column(db.Text)
    is_encrypted = db.Column(db.Boolean, default=False)

    payloads = db.relationship('Payload',
                               secondary=profile_payloads,
                               backref='profiles')

    tags = db.relationship('Tag',
                           secondary=profile_tags,
                           backref='profiles')

