from marshmallow import Schema, fields, post_load
from .models import ADCertPayload


class ConsentTextSchema(Schema):
    en = fields.String(attribute='consent_en')


class ProfileSchema(Schema):
    PayloadDescription = fields.Str(attribute='description')
    PayloadDisplayName = fields.Str(attribute='display_name')
    PayloadExpirationDate = fields.DateTime(attribute='expiration_date')
    PayloadIdentifier = fields.Str(attribute='identifier', required=True)
    PayloadOrganization = fields.Str(attribute='organization')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadRemovalDisallowed = fields.Bool(attribute='removal_disallowed')
    PayloadType = fields.String(default='Configuration', required=True)
    PayloadVersion = fields.Integer(attribute='version', default=1, required=True)
    PayloadScope = fields.String()
    RemovalDate = fields.DateTime(attribute='removal_date')
    DurationUntilRemoval = fields.Float(attribute='duration_until_removal')
    ConsentText = fields.Nested(ConsentTextSchema())


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
        return ADCertPayload(**data)
