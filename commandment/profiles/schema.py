"""
This module defines marshmallow schemas for use in converting .mobileconfig (plist) representations into SQLAlchemy
model representations.
"""

from typing import Union, Callable, Type, List
import plistlib
from marshmallow import Schema, fields, post_load, post_dump
from marshmallow_enum import EnumField
from commandment.profiles import models
from commandment.profiles.energy import ScheduledPowerEventType
from commandment.profiles.certificates import KeyUsage
from commandment.profiles.eap import TTLSInnerAuthentication
from . import PayloadScope

_schemas = {}
"""Hold all registered schemas by their PayloadType."""


def schema_for(payload_type: str) -> Union[None, Type[Schema]]:
    """Get a class that represents the marshmallow schema for a payload, using the payload type.
    
    Args:
          payload_type (str): The value of PayloadType
    Returns:
          None or a class that represents a schema for that payload.
    """
    return _schemas.get(payload_type, None)


def register_payload_schema(payload_type: str) -> Callable[[Type[Schema]], Type[Schema]]:
    """Decorate a Payload schema to register its type. For use with schema_for."""
    def wrapper(cls: Type[Schema]) -> Type[Schema]:
        _schemas[payload_type] = cls
        return cls
        
    return wrapper


class Payload(Schema):
    PayloadType = fields.Str(attribute='type')
    PayloadVersion = fields.Integer(attribute='version')
    PayloadIdentifier = fields.String(attribute='identifier')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadDisplayName = fields.String(attribute='display_name')
    PayloadDescription = fields.String(attribute='description')
    PayloadOrganization = fields.String(attribute='organization')


class ConsentTextSchema(Schema):
    en = fields.String(attribute='consent_en')


@register_payload_schema('com.apple.security.pem')
class CertificatePayloadSchema(Payload):
    PayloadCertificateFileName = fields.Str(attribute='certificate_file_name')
    PayloadContent = fields.Raw(attribute='payload_content')
    Password = fields.Str(attribute='password')

# @register_payload_schema('com.apple.ADCertificate.managed')
# class ADCertificatePayload(Payload):
#     Description = fields.Str(attribute='description')
#     CertServer = fields.Str(attribute='cert_server')
#     CertTemplate = fields.Str(attribute='cert_template')
#     CertificateAuthority = fields.Str(attribute='certificate_authority')
#     CertificateAcquisitionMechanism = EnumField(ADCertificateAcquisitionMechanism, attribute='acquisition_mechanism')
#     CertificateRenewalTimeInterval = fields.Int(attribute='renewal_time_interval')
#     Keysize = fields.Int(attribute='keysize')
#     UserName = fields.Str(attribute='username')
#     Password = fields.Str(attribute='password')
#     PromptForCredentials = fields.Bool(attribute='prompt_for_credentials')
#     AllowAllAppsAccess = fields.Bool(attribute='allow_all_apps_access')
#     KeyIsExtractable = fields.Bool(attribute='key_is_extractable')
#
#     @post_load
#     def make_payload(self, data) -> models.ADCertPayload:
#         return models.ADCertPayload(**data)


class QoSMarkingPolicy(Schema):
    # QoSMarkingWhitelistedAppIdentifiers = fields.Array
    QoSMarkingAppleAudioVideoCalls = fields.Boolean()
    QoSMarkingEnabled = fields.Boolean()


class EAPClientConfiguration(Schema):
    """EAPOLClient configuration properties.
    
    I have added several more unpublished properties from the EAP8012X source available via opensource.apple.com.
    """

    UserName = fields.String()
    UserPassword = fields.String()
    UserPasswordKeychainItemID = fields.String()  # Unconfirmed
    OneTimeUserPassword = fields.Boolean()  # Unconfirmed
    OneTimePassword = fields.Boolean()
    # AcceptEAPTypes = fields.Integer()
    # InnerAcceptEAPTypes  # Unconfirmed
    # PayloadCertificateAnchorUUID = fields.UUID()
    # TLSTrustedServerNames 
    TLSAllowTrustExceptions = fields.Boolean()
    TLSCertificateIsRequired = fields.Boolean()
    """- TLS-based authentication protocol requires a certificate to authenticate
       - the default value is TRUE for EAP-TLS, FALSE otherwise
       - allows for two-factor authentication (certificate + name/password)  
         when set to TRUE for EAP-TTLS, PEAP, EAP-FAST
       - allows for zero-factor authentication when set to FALSE for EAP-TLS"""
    # TLSTrustedCertificates array<data> Unconfirmed
    # TLSSaveTrustExceptions
    # TLSTrustExceptionsDomain
    # exceptions domain values:
    # WirelessSSID
    # ProfileID
    # NetworkInterfaceName  

    # TLSTrustExceptionsID
    # SaveCredentialsOnSuccessfulAuthentication
    # TLSVerifyServerCertificate
    # TLSEnableSessionResumption
    # TLSUserTrustProceedCertificateChain
    # SystemModeUseOpenDirectoryCredentials
    # SystemModeOpenDirectoryNodeName
    
    
    NewPassword = fields.String()
    OuterIdentity = fields.String()
    """OuterIdentity: Applies to TTLS, PEAP, EAP-FAST."""

    TLSIdentityHandle = fields.String()
    """TLSIdentityHandle: TLS only"""

    

    SystemModeCredentialsSource = fields.String()
    TTLSInnerAuthentication = EnumField(TTLSInnerAuthentication)

    # EAP-FAST
    EAPFASTUsePAC = fields.Boolean()
    EAPFASTProvisionPAC = fields.Boolean()
    EAPFASTProvisionPACAnonymously = fields.Boolean()
    EAPSIMNumberOfRANDs = fields.Integer()

    # InnerEAPType
    # InnerEAPTypeName
    # TLSServerCertificateChain

    # To Check: In EAP8012X source
    # SystemModeUseOpenDirectoryCredentials
    # SystemModeOpenDirectoryNodeName
    # 


@register_payload_schema('com.apple.security.scep')
class SCEPPayload(Payload):
    URL = fields.URL(attribute='url')
    Name = fields.String(attribute='name')
    # Subject = fields.Nested()
    Challenge = fields.String(attribute='challenge')
    Keysize = fields.Integer(attribute='key_size')
    CAFingerprint = fields.String(attribute='ca_fingerprint')
    KeyType = fields.String(attribute='key_type')
    KeyUsage = EnumField(KeyUsage, attribute='key_usage')
    # SubjectAltName = fields.Dict(attribute='subject_alt_name')
    Retries = fields.Integer(attribute='retries')
    RetryDelay = fields.Integer(attribute='retry_delay')

    @post_dump(pass_many=False)
    def wrap_payload_content(self, data: dict) -> dict:
        """SCEP Payload is silly and double wraps its PayloadContent item."""
        inner_content = {
            'URL': data.pop('URL', None),
            'Name': data.pop('Name'),
            'Challenge': data.pop('Challenge'),
            'Keysize': data.pop('Keysize'),
            'CAFingerprint': data.pop('CAFingerprint'),
            'KeyType': data.pop('KeyType'),
            'KeyUsage': data.pop('KeyUsage'),
            'Retries': data.pop('Retries'),
            'RetryDelay': data.pop('RetryDelay'),
        }

        data['PayloadContent'] = inner_content
        return data

    @post_load
    def make_payload(self, data: dict) -> models.SCEPPayload:
        return models.SCEPPayload(**data)

#
# @register_payload_schema('com.apple.wifi.managed')
# class WIFIPayload(Payload):
#     SSID_STR = fields.Str(attribute='ssid_str')
#     HIDDEN_NETWORK = fields.Boolean(attribute='hidden_network')
#     AutoJoin = fields.Boolean(attribute='auto_join', allow_none=True)
#     EncryptionType = EnumField(WIFIEncryptionType, attribute='encryption_type')
#     IsHotspot = fields.Boolean(attribute='is_hotspot', allow_none=True)
#     DomainName = fields.String(attribute='domain_name', allow_none=True)
#     ServiceProviderRoamingEnabled = fields.Boolean(attribute='service_provider_roaming_enabled', allow_none=True)
#     # RoamingConsortiumOIs = fields.Nested(fields.String(), many=True)
#     # NAIRealmNames
#     # MCCAndMNCs
#     DisplayedOperatorName = fields.String(attribute='displayed_operator_name', allow_none=True)
#     ProxyType = fields.String(attribute='proxy_type', allow_none=True)
#     CaptiveBypass = fields.Boolean(attribute='captive_bypass', allow_none=True)
#     QoSMarkingPolicy = fields.Nested(QoSMarkingPolicy(), allow_none=True)
#
#     Password = fields.String(attribute='password', allow_none=True)
#     PayloadCertificateUUID = fields.UUID(attribute='payload_certificate_uuid', allow_none=True)
#     EAPClientConfiguration = fields.Nested(EAPClientConfiguration(), allow_none=True)
#
#     @post_load
#     def make_payload(self, data: dict) -> models.WIFIPayload:
#         payload = models.WIFIPayload(**data)
#         return payload


class EnergySaverSettings(Schema):
    AutomaticRestartOnPowerLoss = fields.Integer(load_from='Automatic Restart On Power Loss')  # Pseudo boolean 0/1
    DiskSleepTimerBoolean = fields.Boolean(load_from='Disk Sleep Timer-boolean')
    DiskSleepTimer = fields.Integer(load_from='Display Sleep Timer')
    SystemSleepTimer = fields.Integer(load_from='System Sleep Timer')
    WakeOnLAN = fields.Integer(load_from='Wake On LAN')  # Pseudo boolean 0/1


class EnergySaverPowerSchedule(Schema):
    eventtype = EnumField(ScheduledPowerEventType)
    time = fields.Integer(validate=lambda n: 0 <= n <= 2400)
    weekdays = fields.Integer()


class EnergySaverSchedules(Schema):
    RepeatingPowerOn = fields.Nested(EnergySaverPowerSchedule)
    RepeatingPowerOff = fields.Nested(EnergySaverPowerSchedule)


@register_payload_schema('com.apple.MCX')
class EnergySaverPayload(Payload):
    DestroyFVKeyOnStandby = fields.Boolean(attribute='destroy_fv_key_on_standby')
    SleepDisabled = fields.Boolean(attribute='sleep_disabled')
    DesktopACPowerProfileNumber = fields.Integer(load_from='com.apple.EnergySaver.desktop.ACPower-ProfileNumber')
    PortableACPowerProfileNumber = fields.Integer(load_from='com.apple.EnergySaver.portable.ACPower-ProfileNumber')
    PortableBatteryProfileNumber = fields.Integer(load_from='com.apple.EnergySaver.portable.BatteryPower-ProfileNumber')
    DesktopACPower = fields.Nested(EnergySaverSettings, load_from='com.apple.EnergySaver.desktop.ACPower')
    PortableACPower = fields.Nested(EnergySaverSettings, load_from='com.apple.EnergySaver.portable.ACPower')
    PortableBatteryPower = fields.Nested(EnergySaverSettings, load_from='com.apple.EnergySaver.portable.BatteryPower')
    Schedule = fields.Nested(EnergySaverSchedules, load_from='com.apple.EnergySaver.desktop.Schedule')


@register_payload_schema('com.apple.mdm')
class MDMPayload(Payload):
    IdentityCertificateUUID = fields.UUID(attribute='identity_certificate_uuid', required=True)
    Topic = fields.String(attribute='topic', required=True)
    ServerURL = fields.URL(attribute='server_url', required=True)
    # ServerCapabilities = fields.Nested(many=True)
    SignMessage = fields.Boolean(attribute='sign_message')
    CheckInURL = fields.String(attribute='check_in_url')
    CheckOutWhenRemoved = fields.Boolean(attribute='check_out_when_removed')
    AccessRights = fields.Integer(attribute='access_rights')
    UseDevelopmentAPNS = fields.Boolean(attribute='use_development_apns')

    @post_load
    def make_payload(self, data: dict) -> models.MDMPayload:
        return models.MDMPayload(**data)


class ProfileSchema(Schema):
    PayloadDescription = fields.Str(attribute='description')
    PayloadDisplayName = fields.Str(attribute='display_name')
    PayloadExpirationDate = fields.DateTime(attribute='expiration_date')
    PayloadIdentifier = fields.Str(attribute='identifier', required=True)
    PayloadOrganization = fields.Str(attribute='organization')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadRemovalDisallowed = fields.Bool(attribute='removal_disallowed')
    PayloadType = fields.Function(lambda obj: 'Configuration', attribute='payload_type')
    PayloadVersion = fields.Function(lambda obj: 1, attribute='version')
    PayloadScope = EnumField(PayloadScope, attribute='scope')
    RemovalDate = fields.DateTime(attribute='removal_date')
    DurationUntilRemoval = fields.Float(attribute='duration_until_removal')
    ConsentText = fields.Nested(ConsentTextSchema())
    PayloadContent = fields.Method('get_payloads', deserialize='load_payloads')

    def get_payloads(self, obj):
        payloads = []

        for payload in obj.payloads:
            schema = schema_for(payload.type)
            if schema is not None:
                result = schema().dump(payload)
                payloads.append(result.data)
            else:
                print('Unsupported PayloadType: {}'.format(payload.type))

        return payloads

    def load_payloads(self, payload_content: list) -> List[Schema]:
        payloads = []

        for content in payload_content:
            schema = schema_for(content['PayloadType'])
            if schema is not None:
                result = schema().load(content)
                payloads.append(result.data)
            else:
                print('Unsupported PayloadType: {}'.format(content['PayloadType']))

        return payloads


    @post_load
    def make_profile(self, data):
        payloads = data.pop('PayloadContent', [])
        p = models.Profile(**data)
        # for pl in payloads:
        #     p.payloads.append(pl)

        return p