"""
This module defines marshmallow schemas for use in converting .mobileconfig (plist) representations into SQLAlchemy
model representations.
"""

from marshmallow import Schema, fields, post_load
from commandment.profiles import models


class ConsentTextSchema(Schema):
    en = fields.String(attribute='consent_en')




class ADCertificatePayload(Schema):
    Description = fields.Str(attribute='description')
    CertServer = fields.Str(attribute='cert_server')
    CertTemplate = fields.Str(attribute='cert_template')
    CertificateAuthority = fields.Str(attribute='certificate_authority')
    CertificateAcquisitionMechanism = fields.Str(attribute='acquisition_mechanism')
    CertificateRenewalTimeInterval = fields.Int(attribute='renewal_time_interval')
    Keysize = fields.Int(attribute='keysize')
    UserName = fields.Str(attribute='username')
    Password = fields.Str(attribute='password')
    PromptForCredentials = fields.Bool(attribute='prompt_for_credentials')
    AllowAllAppsAccess = fields.Bool(attribute='allow_all_apps_access')
    KeyIsExtractable = fields.Bool(attribute='key_is_extractable')
    
    @post_load
    def make_payload(self, data):
        return models.ADCertPayload(**data)


class QoSMarkingPolicy(Schema):
    # QoSMarkingWhitelistedAppIdentifiers = fields.Array
    QoSMarkingAppleAudioVideoCalls = fields.Boolean()
    QoSMarkingEnabled = fields.Boolean()


class EAPClientConfiguration(Schema):
    UserName = fields.String()
    # AcceptEAPTypes = fields.Integer()
    UserPassword = fields.String()
    OneTimePassword = fields.Boolean()
    # PayloadCertificateAnchorUUID = fields.UUID()
    # TLSTrustedServerNames
    TLSAllowTrustExceptions = fields.Boolean()
    TLSCertificateIsRequired = fields.Boolean()
    OuterIdentity = fields.String()
    TTLSInnerAuthentication = fields.String()

    # EAP-FAST
    EAPFASTUsePAC = fields.Boolean()
    EAPFASTProvisionPAC = fields.Boolean()
    EAPFASTProvisionPACAnonymously = fields.Boolean()
    EAPSIMNumberOfRANDs = fields.Integer()


class Payload(Schema):
    PayloadType = fields.Str(attribute='type')
    PayloadVersion = fields.Integer(attribute='version')
    PayloadIdentifier = fields.String(attribute='identifier')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadDisplayName = fields.String(attribute='display_name')
    PayloadDescription = fields.String(attribute='description')
    PayloadOrganization = fields.String(attribute='organization')


class WIFIPayload(Payload):


    SSID_STR = fields.Str(attribute='ssid_str')
    HIDDEN_NETWORK = fields.Boolean(attribute='hidden_network')
    AutoJoin = fields.Boolean(attribute='auto_join', allow_none=True)
    EncryptionType = fields.Str(attribute='encryption_type')
    IsHotspot = fields.Boolean(attribute='is_hotspot', allow_none=True)
    DomainName = fields.String(attribute='domain_name', allow_none=True)
    ServiceProviderRoamingEnabled = fields.Boolean(attribute='service_provider_roaming_enabled', allow_none=True)
    # RoamingConsortiumOIs = fields.Nested(fields.String(), many=True)
    # NAIRealmNames
    # MCCAndMNCs
    DisplayedOperatorName = fields.String(attribute='displayed_operator_name', allow_none=True)
    ProxyType = fields.String(attribute='proxy_type', allow_none=True)
    CaptiveBypass = fields.Boolean(attribute='captive_bypass', allow_none=True)
    QoSMarkingPolicy = fields.Nested(QoSMarkingPolicy(), allow_none=True)

    Password = fields.String(attribute='password', allow_none=True)
    PayloadCertificateUUID = fields.UUID(attribute='payload_certificate_uuid', allow_none=True)
    EAPClientConfiguration = fields.Nested(EAPClientConfiguration(), allow_none=True)

    @post_load
    def make_payload(self, data: dict) -> models.WIFIPayload:
        payload = models.WIFIPayload(**data)
        return payload


class ProfileSchema(Schema):
    PayloadDescription = fields.Str(attribute='description')
    PayloadDisplayName = fields.Str(attribute='display_name')
    PayloadExpirationDate = fields.DateTime(attribute='expiration_date')
    PayloadIdentifier = fields.Str(attribute='identifier', required=True)
    PayloadOrganization = fields.Str(attribute='organization')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadRemovalDisallowed = fields.Bool(attribute='removal_disallowed')
    # PayloadType = fields.String(attribute='payload_type', default='Configuration', required=True)
    PayloadVersion = fields.Integer(attribute='version', default=1, required=True)
    PayloadScope = fields.String(attribute='scope')
    RemovalDate = fields.DateTime(attribute='removal_date')
    DurationUntilRemoval = fields.Float(attribute='duration_until_removal')
    ConsentText = fields.Nested(ConsentTextSchema())

    PayloadContent = fields.Method('get_payloads', deserialize='load_payloads')

    def get_payloads(self, obj):
        return None

    def load_payloads(self, payload_content: list):
        payloads = []

        for content in payload_content:
            if content['PayloadType'] == 'com.apple.wifi.managed':
                result = WIFIPayload().load(content)
                payloads.append(result.data)

        return payloads


    @post_load
    def make_profile(self, data):
        payloads = data.pop('PayloadContent', [])
        p = models.Profile(**data)
        for pl in payloads:
            p.payloads.append(pl)

        return p