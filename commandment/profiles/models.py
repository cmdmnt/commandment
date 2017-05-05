from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, DateTime, Enum as DBEnum, text, \
    BigInteger, and_, or_, LargeBinary
from sqlalchemy.orm import relationship

from commandment.profiles.ad import ADMountStyle, ADNamespace, ADPacketSignPolicy, ADPacketEncryptPolicy, \
    ADCertificateAcquisitionMechanism
from commandment.profiles.email import EmailAuthenticationType, EmailAccountType
from commandment.profiles.vpn import VPNType
from commandment.profiles.wifi import WIFIEncryptionType, WIFIProxyType
from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4
from .cert import KeyUsage
from . import PayloadScope

from ..models import db

payload_dependencies = Table('payload_dependencies', db.metadata,
                             Column('payload_uuid', GUID, ForeignKey('payloads.uuid')),
                             Column('depends_on_payload_uuid', GUID, ForeignKey('payloads.uuid')),
                             )


class Payload(db.Model):
    __tablename__ = 'payloads'

    id = Column(Integer, primary_key=True)
    type = Column(String, index=True, nullable=False)
    version = Column(Integer)
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


class ADCertPayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    certificate_description = Column(String)  # Description was reserved from the base Payload table
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


# class EAPClientConfiguration(db.Model):
#     __table__ = 'eap_client_configurations'
#
#     id = Column(Integer, primary_key=True)
    # accept_eap_types
    # payload_id = Column(Integer, ForeignKey('payloads.id'))
    #user_name = Column(String)
    #user_password = Column(String)
    #one_time_password = Column(Boolean)
    # payload_certificate_anchor_uuid
    # tls_trusted_server_names
    #tls_allow_trust_exceptions = Column(Boolean)
    #ttls_inner_authentication = Column(String)
    #outer_identity = Column(String)
    #system_mode_credentials_source = Column(String)
    #eap_fast_use_pac = Column(Boolean)
    #eap_fast_provision_pac = Column(Boolean)
    #eap_fast_provision_pac_anonymously = Column(Boolean)
    #eap_sim_number_of_rands = Column(Integer)


class WIFIPayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    ssid_str = Column(String, nullable=False)
    hidden_network = Column(Boolean, default=False)
    auto_join = Column(Boolean, nullable=True)
    encryption_type = Column(DBEnum(WIFIEncryptionType), default=WIFIEncryptionType.Any)
    is_hotspot = Column(Boolean)
    domain_name = Column(String)
    service_provider_roaming_enabled = Column(Boolean)

    roaming_consortium_ois = Column(String) # JSON
    nai_realm_names = Column(String) # JSON
    mccs_and_mncs = Column(String) # JSON
    displayed_operator_name = Column(String)
    captive_bypass = Column(Boolean)

    # If WEP, WPA or Any
    password = Column(String)
    #eap_client_configuration_id = Column(Integer, ForeignKey('eap_client_configurations.id'))
    tls_certificate_required = Column(Boolean)
    payload_certificate_uuid = Column(GUID)

    # Manual Proxy
    proxy_type = Column(String)
    proxy_server = Column(String)
    proxy_server_port = Column(Integer)
    proxy_username = Column(String)
    proxy_password = Column(String)
    proxy_pac_url = Column(String)
    proxy_pac_fallback_allowed = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.wifi.managed',
    }


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


class CertificatePayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    certificate_file_name = Column(String)
    payload_content = Column(LargeBinary)
    password = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.security.pem'
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


class PasswordPolicyPayload(Payload):
    id = Column(Integer, ForeignKey('payloads.id'), primary_key=True)
    allow_simple = Column(Boolean)
    force_pin = Column(Boolean)
    max_failed_attempts = Column(Integer)
    max_inactivity = Column(Integer)
    max_pin_age_in_days = Column(Integer)
    min_complex_chars = Column(Integer)
    min_length = Column(Integer)
    require_alphanumeric = Column(Boolean)
    pin_history = Column(Integer)
    max_grace_period = Column(Integer)
    allow_fingerprint_modification = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'com.apple.mobiledevice.passwordpolicy'
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
    description = Column(Text)
    display_name = Column(String)
    expiration_date = Column(DateTime)  # Only for old style OTA
    identifier = Column(String, nullable=False)
    organization = Column(String)
    uuid = Column(GUID, index=True, default=uuid4())
    removal_disallowed = Column(Boolean)
    version = Column(Integer, default=1)
    scope = Column(DBEnum(PayloadScope), default=PayloadScope.User.value)
    removal_date = Column(DateTime)
    duration_until_removal = Column(BigInteger)
    consent_en = Column(Text)
    is_encrypted = Column(Boolean, default=False)

    payloads = relationship('Payload',
                            secondary=profile_payloads,
                            backref='profiles')
