from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from enum import IntFlag
from .. import models


class ErrorChainItem(Schema):
    LocalizedDescription = fields.String()
    USEnglishDescription = fields.String()
    ErrorDomain = fields.String()
    ErrorCode = fields.Number()


class CommandResponse(Schema):
    Status = fields.String()
    UDID = fields.UUID()
    CommandUUID = fields.UUID()
    ErrorChain = fields.Nested(ErrorChainItem, many=True)


class ProfileListResponse(CommandResponse):
    pass


class HardwareEncryptionCaps(IntFlag):
    BlockLevelEncryption = 1
    FileLevelEncryption = 2

    All = BlockLevelEncryption | FileLevelEncryption


class FirewallApplicationItem(Schema):
    BundleID = fields.String()
    Allowed = fields.Boolean()
    Name = fields.String()


class FirewallSettings(Schema):
    FirewallEnabled = fields.Boolean()
    BlockAllIncoming = fields.Boolean()
    StealthMode = fields.Boolean()
    Applications = fields.Nested(FirewallApplicationItem, many=True)


class SecurityInfoResponse(CommandResponse):
    HardwareEncryptionCaps = EnumField(HardwareEncryptionCaps)
    PasscodePresent = fields.Boolean()
    PasscodeCompliant = fields.Boolean()
    PasscodeCompliantWithProfiles = fields.Boolean()
    PasscodeLockGracePeriodEnforced = fields.Integer()
    FDE_Enabled = fields.Boolean()
    FDE_HasPersonalRecoveryKey = fields.Boolean()
    FDE_HasInstitutionalRecoveryKey = fields.Boolean()
    FirewallSettings = fields.Nested(FirewallSettings)
    SystemIntegrityProtectionEnabled = fields.Boolean()


class InstalledApplication(Schema):
    Identifier = fields.String()
    Version = fields.String()
    ShortVersion = fields.String()
    Name = fields.String()
    BundleSize = fields.Integer()
    DynamicSize = fields.Integer()
    IsValidated = fields.Boolean()

    @post_load
    def make_installed_application(self, data: dict) -> models.InstalledApplication:
        return models.InstalledApplication(**data)


class InstalledApplicationListResponse(CommandResponse):
    InstalledApplicationList = fields.Nested(InstalledApplication, many=True)


class CertificateListItem(Schema):
    CommonName = fields.String()
    IsIdentity = fields.Boolean()
    Data = fields.String()

    @post_load
    def make_installed_certificate(self, data: dict) -> models.InstalledCertificate:
        return models.InstalledCertificate(**data)


class CertificateListResponse(CommandResponse):
    CertificateList = fields.Nested(CertificateListItem, many=True)


