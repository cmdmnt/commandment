
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
