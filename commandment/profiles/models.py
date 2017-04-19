from enum import Enum, Flag, auto
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, DateTime, Enum as DBEnum, text, \
    BigInteger, and_, or_, LargeBinary
from sqlalchemy.orm import relationship

from commandment.profiles.ad import ADMountStyle, ADNamespace, ADPacketSignPolicy, ADPacketEncryptPolicy
from commandment.profiles.wifi import WIFIEncryptionType, WIFIProxyType
from ..dbtypes import GUID, JSONEncodedDict
from biplist import Data as NSData, readPlistFromString
from uuid import uuid4
from .cert import KeyUsage
from . import PayloadScope

from ..models import db

payload_dependencies = Table('payload_dependencies', db.metadata,
                             Column('payload_uuid', GUID, ForeignKey('payloads.uuid')),
                             Column('depends_on_payload_uuid', GUID, ForeignKey('payloads.uuid')),
                             )


class Payload(db.Model):
    """Configuration Profile Payload"""
    __tablename__ = 'payloads'

    id = Column(Integer, primary_key=True)
    type = Column(String, index=True, nullable=False)
    version = Column(Integer, nullable=True)
    uuid = Column(GUID, index=True, default=uuid4())
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    organization = Column(String, nullable=True)

    # Dependencies should be tracked in cases where the payload refers to another required payload.
    # eg. a reference to certificate payload in an 802.1x configuration.
    # depends_on = relationship("Payload",
    #                           secondary=payload_dependencies,
    #                           backref="dependents")

    __mapper_args__ = {
        'polymorphic_identity': 'payload',
        'polymorphic_on': type,
    }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a new payload from its PayloadData dict.

        Returns:
              Payload: An instance of the payload model.
        """
        if data['PayloadType'] != 'com.apple.security.scep':
            return None

        return SCEPPayload.from_dict(data)


class SCEPPayload(Payload):
    """SCEP Payload ``com.apple.security.scep``"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, nullable=True)
    subject = Column(String, nullable=False)  # eg. O=x/OU=y/CN=z
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

    @classmethod
    def from_dict(cls, data: dict):
        pp = cls()
        pp.uuid = data.get('PayloadUUID', None)
        pp.display_name = data.get('PayloadDisplayName', None)
        pp.description = data.get('PayloadDescription', None)
        pp.organization = data.get('PayloadOrganization', None)

        content = data['PayloadContent']

        pp.url = content.get('URL')
        pp.name = content.get('Name', None)
        #pp.subject = '/'.join(data.get('Subject', []))
        pp.subject = 'NOT=IMPLEMENTED'
        pp.challenge = content.get('Challenge', None)
        pp.key_size = content.get('Keysize', None)
        pp.ca_fingerprint = content.get('CAFingerprint', None)
        pp.key_type = 'RSA'
        pp.key_usage = KeyUsage(content.get('KeyUsage', KeyUsage.All.value))
        pp.retries = content.get('Retries', 3)
        pp.retry_delay = content.get('RetryDelay', 10)
        pp.certificate_renewal_time_interval = content.get('CertificateRenewalTimeInterval', 14)
        # GetCACaps ignored

        return pp


class ADCertificateAcquisitionMechanism(Enum):
    RPC = 'RPC'
    HTTP = 'HTTP'


class ADCertPayload(Payload):
    """Active Directory Certificate Payload"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    allow_all_apps_access = Column(Boolean)
    cert_server = Column(String, nullable=False)
    cert_template = Column(String, nullable=False, default='User')
    acquisition_mechanism = Column(DBEnum(ADCertificateAcquisitionMechanism), default=ADCertificateAcquisitionMechanism.RPC)
    certificate_authority = Column(String, nullable=False)
    renewal_time_interval = Column(Integer)
    identity_description = Column(String, nullable=True)
    key_is_extractable = Column(Boolean, default=False)
    prompt_for_credentials = Column(Boolean)
    keysize = Column(Integer, default=2048)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.ADCertificate.managed',
    }


class ADPayload(Payload):
    """Active Directory Join Payload"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    host_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    ad_organizational_unit = Column(String, nullable=False)
    ad_mount_style = Column(DBEnum(ADMountStyle), nullable=False)
    ad_default_user_shell = Column(String)
    ad_map_uid_attribute = Column(String)
    ad_map_gid_attribute = Column(String)
    ad_map_ggid_attribute = Column(String)
    ad_preferred_dc_server = Column(String)
    ad_domain_admin_group_list = Column(String) # JSON
    ad_namespace = Column(DBEnum(ADNamespace), default=ADNamespace.Domain)
    ad_packet_sign = Column(DBEnum(ADPacketSignPolicy), default=ADPacketSignPolicy.Allow)
    ad_packet_encrypt = Column(DBEnum(ADPacketEncryptPolicy), default=ADPacketEncryptPolicy.Allow)
    ad_restrict_ddns = Column(String)  # JSON
    ad_trust_change_pass_interval = Column(Integer)

    # We will take null to mean that the flag is not set
    ad_create_mobile_account_at_login = Column(Boolean)
    ad_warn_user_before_creating_ma = Column(Boolean)
    ad_force_home_local = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.DirectoryService.managed',
    }


class WIFIPayload(Payload):
    """Wi-Fi Payload"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    ssid_str = Column(String, nullable=False)
    hidden_network = Column(Boolean, default=False)
    auto_join = Column(Boolean, nullable=True)
    encryption_type = Column(DBEnum(WIFIEncryptionType), default=WIFIEncryptionType.Any)
    is_hotspot = Column(Boolean, nullable=True)
    domain_name = Column(String, nullable=True)
    service_provider_roaming_enabled = Column(Boolean, nullable=True)

    roaming_consortium_ois = Column(String, nullable=True) # JSON
    nai_realm_names = Column(String, nullable=True) # JSON
    mccs_and_mncs = Column(String, nullable=True) # JSON
    displayed_operator_name = Column(String, nullable=True)
    proxy_type = Column(DBEnum(WIFIProxyType), nullable=True)
    captive_bypass = Column(Boolean, nullable=True)

    # If WEP, WPA or Any
    password = Column(String, nullable=True)
    eap_client_configuration = Column(String)  # JSON
    payload_certificate_uuid = Column(GUID, nullable=True)

    # Manual Proxy
    proxy_server = Column(String, nullable=True)
    proxy_server_port = Column(Integer, nullable=True)
    proxy_username = Column(String, nullable=True)
    proxy_password = Column(String, nullable=True)
    proxy_pac_url = Column(String, nullable=True)
    proxy_pac_fallback_allowed = Column(Boolean, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.wifi.managed',
    }


class VPNType(Enum):
    L2TP = 'L2TP'
    PPTP = 'PPTP'
    IPSec = 'IPSec'
    IKEv2 = 'IKEv2'
    AlwaysOn = 'AlwaysOn'
    VPN = 'VPN'


class VPNPayload(Payload):
    """VPN Payload"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    user_defined_name = Column(String)
    override_primary = Column(Boolean, default=False)
    vpn_type = Column(DBEnum(VPNType), nullable=False)
    vpn_sub_type = Column(String)
    provider_bundle_identifier = Column(String)
    on_demand_enabled = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.vpn.managed',
    }


class EmailAccountType(Enum):
    POP = 'EmailTypePOP'
    IMAP = 'EmailTypeIMAP'


class EmailAuthenticationType(Enum):
    Password = 'EmailAuthPassword'
    CRAM_MD5 = 'EmailAuthCRAMMD5'
    NTLM = 'EmailAuthNTLM'
    HTTP_MD5 = 'EmailAuthHTTPMD5'
    ENone = 'EmailAuthNone'


class EmailPayload(Payload):
    """E-mail Payload"""
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    email_account_description = Column(String)
    email_account_name = Column(String)
    email_account_type = Column(DBEnum(EmailAccountType), nullable=False)
    email_address = Column(String)
    incoming_auth = Column(DBEnum(EmailAuthenticationType), nullable=False)
    incoming_host = Column(String, nullable=False)
    incoming_port = Column(Integer)
    incoming_use_ssl = Column(Boolean, default=False)
    incoming_username = Column(String, nullable=False)
    incoming_password = Column(String)
    outgoing_password = Column(String)
    outgoing_incoming_same = Column(Boolean)
    outgoing_auth = Column(DBEnum(EmailAuthenticationType), nullable=False)
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.mail.managed'
    }

profile_payloads = Table('profile_payloads', db.metadata,
                         Column('profile_id', Integer, ForeignKey('profiles.id')),
                         Column('payload_id', Integer, ForeignKey('payloads.id')))


class Profile(db.Model):
    """Top level profile.

    In Commandment, multiple profiles may have an association with the same payload.

    See Also:
          - `Configuration Profile Keys
            <https://developer.apple.com/library/content/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html#//apple_ref/doc/uid/TP40010206-CH1-SW7>`_.

    Attributes:
        
    """
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    display_name = Column(String, nullable=True)
    expiration_date = Column(DateTime, nullable=True)  # Only for old style OTA
    identifier = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    uuid = Column(GUID, index=True, default=uuid4())
    removal_disallowed = Column(Boolean, nullable=True)
    version = Column(Integer, default=1)
    scope = Column(DBEnum(PayloadScope), default=PayloadScope.User.value, nullable=True)
    removal_date = Column(DateTime, nullable=True)
    duration_until_removal = Column(BigInteger, nullable=True)
    consent_en = Column(Text, nullable=True)
    is_encrypted = Column(Boolean, default=False)

    payloads = relationship('Payload',
                            secondary=profile_payloads,
                            backref='profiles')

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create an instance of ``Profile`` from a Configuration Profile as bytes.

        Returns:
              Profile: The configuration profile, with Payload objects created for each payload.
        """
        plist_data = readPlistFromString(data)
        p = cls()
        if 'PayloadDescription' in plist_data:
            p.description = plist_data['PayloadDescription']

        if 'PayloadDisplayName' in plist_data:
            p.display_name = plist_data['PayloadDisplayName']

        if 'PayloadExpirationDate' in plist_data:
            p.expiration_date = plist_data['PayloadExpirationDate']

        if 'PayloadIdentifier' in plist_data:
            p.identifier = plist_data['PayloadIdentifier']

        if 'PayloadOrganization' in plist_data:
            p.organization = plist_data['PayloadOrganization']

        if 'PayloadUUID' in plist_data:
            p.uuid = plist_data['PayloadUUID']

        if 'PayloadRemovalDisallowed' in plist_data:
            p.removal_disallowed = plist_data['PayloadRemovalDisallowed']

        if 'PayloadScope' in plist_data:
            p.scope = PayloadScope(plist_data['PayloadScope']).value

        if 'RemovalDate' in plist_data:
            p.removal_date = plist_data['PayloadRemovalDate']

        if 'DurationUntilRemoval' in plist_data:
            p.duration_until_removal = plist_data['DurationUntilRemoval']

        if 'ConsentText' in plist_data and 'en' in plist_data['ConsentText']:
            p.consent_en = plist_data['ConsentText']['en']

        # TODO: Some profiles can contain keys outside of PayloadData so we will have to calculate the intersection
        # between the previous attributes and the remainder

        if 'PayloadContent' in plist_data:
            for payload_dict in plist_data['PayloadContent']:
                pl = Payload.from_dict(payload_dict)
                if pl is not None:
                    p.payloads.append(pl)

        return p
