from cryptography import x509
from commandment.dep import SetupAssistantStep, SkipSetupSteps, DEPOrgType, DEPOrgVersion
from commandment.models import db
from commandment.pki.models import CertificateType, Certificate
from commandment.dbtypes import GUID


class DEPServerTokenCertificate(Certificate):
    """DEP Server Token Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.STOKEN.value
    }

    @classmethod
    def from_crypto(cls, certificate: x509.Certificate):
        m = Certificate.from_crypto_type(certificate, CertificateType.STOKEN)
        return m


class DEPAnchorCertificate(Certificate):
    """DEP Anchor Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.ANCHOR.value
    }


class DEPSupervisionCertificate(Certificate):
    """DEP Supervision Certificate"""
    __mapper_args__ = {
        'polymorphic_identity': CertificateType.SUPERVISION.value
    }


class DEPAccount(db.Model):
    """DEP Account

    This table stores information about a single DEP account (aka one 'MDM Server' in the portal),
     and its current token.
    """
    __tablename__ = 'dep_accounts'

    id = db.Column(db.Integer, primary_key=True)

    # certificate for PKI of server token
    certificate_id = db.Column(db.ForeignKey('certificates.id'))
    certificate = db.relationship('DEPServerTokenCertificate', backref='dep_configurations')

    # OAuth creds
    consumer_key = db.Column(db.String())
    consumer_secret = db.Column(db.String())
    access_token = db.Column(db.String())
    access_secret = db.Column(db.String())
    access_token_expiry = db.Column(db.DateTime())

    token_updated_at = db.Column(db.DateTime())

    # Current session token
    auth_session_token = db.Column(db.String())

    # Information synchronised from the /account endpoint
    server_name = db.Column(db.String())
    server_uuid = db.Column(GUID)
    admin_id = db.Column(db.String())
    facilitator_id = db.Column(db.String())
    org_name = db.Column(db.String())
    org_email = db.Column(db.String())
    org_phone = db.Column(db.String())
    org_address = db.Column(db.String())
    org_type = db.Column(db.Enum(*DEPOrgType.__members__.items()))
    org_version = db.Column(db.Enum(*DEPOrgVersion.__members__.items()))
    org_id = db.Column(db.String())
    org_id_hash = db.Column(db.String())

    url = db.Column(db.String())

    # Hold the state of the in-progress fetch/sync in case the DEP thread dies
    cursor = db.Column(db.String())
    more_to_follow = db.Column(db.Boolean())
    fetched_until = db.Column(db.DateTime())


dep_profile_anchor_certificates = db.Table(
    'dep_profile_anchor_certificates',
    db.metadata,
    db.Column('dep_profile_id', db.Integer, db.ForeignKey('dep_profiles.id')),
    db.Column('certificate_id', db.Integer, db.ForeignKey('certificates.id')),
)

dep_profile_supervision_certificates = db.Table(
    'dep_profile_supervision_certificates',
    db.metadata,
    db.Column('dep_profile_id', db.Integer, db.ForeignKey('dep_profiles.id')),
    db.Column('certificate_id', db.Integer, db.ForeignKey('certificates.id')),
)


class DEPProfile(db.Model):
    __tablename__ = 'dep_profiles'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(GUID, index=True)
    profile_name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    allow_pairing = db.Column(db.Boolean)
    is_supervised = db.Column(db.Boolean)
    is_multi_user = db.Column(db.Boolean)
    is_mandatory = db.Column(db.Boolean)
    await_device_configured = db.Column(db.Boolean)
    is_mdm_removable = db.Column(db.Boolean)
    support_phone_number = db.Column(db.String)
    auto_advance_setup = db.Column(db.Boolean)
    support_email_address = db.Column(db.String)
    org_magic = db.Column(db.String)
    skip_setup_items = db.Column(db.Enum(*SetupAssistantStep.__members__.items()))
    department = db.Column(db.String)

    anchor_certs = db.relationship(
        'DEPAnchorCertificate',
        secondary=dep_profile_anchor_certificates,
        #  back_populates='anchor_dep_profiles'
    )

    supervising_host_certs = db.relationship(
        'DEPSupervisionCertificate',
        secondary=dep_profile_supervision_certificates,
        #  back_populates='supervising_dep_profiles'
    )
