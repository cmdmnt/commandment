"""
This module defines marshmallow schemas for use in converting .mobileconfig (plist) representations into SQLAlchemy
model representations.
"""

from typing import Union, Callable, Type, List, Dict
from marshmallow import Schema, fields, post_load, post_dump
from marshmallow_enum import EnumField
from commandment.profiles import models
from commandment.profiles.certificates import KeyUsage
from . import PayloadScope

_schemas: Dict[str, Schema] = {}
"""Hold all registered schemas by their PayloadType."""


def schema_for(payload_type: str) -> Union[None, Type[Schema]]:
    """Get a class that represents the marshmallow schema for a payload, using the payload type.
    
    Args:
          payload_type (str): The value of PayloadType
    Returns:
          None or a class that represents a schema for that payload.
    """
    return _schemas.get(payload_type, None)


def register_payload_schema(*args) -> Callable[[Type[Schema]], Type[Schema]]:
    """Decorate a Payload schema to register its type. For use with schema_for."""
    def wrapper(cls: Type[Schema]) -> Type[Schema]:
        for payload_type in args:
            _schemas[payload_type] = cls
        return cls
        
    return wrapper


class Payload(Schema):
    PayloadType = fields.Str(attribute='type', required=True)
    PayloadVersion = fields.Integer(attribute='version', default=1)
    PayloadIdentifier = fields.String(attribute='identifier')
    PayloadUUID = fields.UUID(attribute='uuid')
    PayloadDisplayName = fields.String(attribute='display_name')
    PayloadDescription = fields.String(attribute='description')
    PayloadOrganization = fields.String(attribute='organization')


@register_payload_schema('Profile Service')
class ProfileServicePayload(Schema):
    URL = fields.URL()
    DeviceAttributes = fields.String(many=True)
    Challenge = fields.String()
    

class ConsentTextSchema(Schema):
    en = fields.String(attribute='consent_en')


@register_payload_schema('com.apple.security.pem', 'com.apple.security.root', 'com.apple.security.pkcs1',
                         'com.apple.security.pkcs12')
class CertificatePayloadSchema(Payload):
    PayloadCertificateFileName = fields.Str(attribute='certificate_file_name')
    PayloadContent = fields.Raw(attribute='payload_content')
    Password = fields.Str(attribute='password')



@register_payload_schema('com.apple.security.scep')
class SCEPPayload(Payload):
    URL = fields.URL(attribute='url')
    Name = fields.String(attribute='name')
    # Subject = fields.Nested()
    Challenge = fields.String(attribute='challenge')
    Keysize = fields.Integer(attribute='key_size')
    CAFingerprint = fields.String(attribute='ca_fingerprint')
    KeyType = fields.String(attribute='key_type')
    KeyUsage = EnumField(KeyUsage, attribute='key_usage', by_value=True)
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