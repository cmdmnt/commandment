"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
import plistlib
from uuid import uuid4
import collections
from enum import Enum, IntFlag

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'


class PayloadScope(Enum):
    User = 'User'
    System = 'System'


class PayloadInvalid(Exception):
    # base class for invalid Payloads
    pass


class PayloadKeyRequired(PayloadInvalid):
    # missing required Payload keys
    pass


class PayloadValueError(PayloadInvalid):
    # Payload keys are not correct value or format
    pass


class DeviceAttributes(Enum):
    """This enumeration describes all of the device attributes available to OTA profile enrolment."""
    UDID = 'UDID'
    VERSION = 'VERSION'
    PRODUCT = 'PRODUCT'
    SERIAL = 'SERIAL'
    MEID = 'MEID'
    IMEI = 'IMEI'
    

PAYLOADS = {}


class PayloadClass(type):
    """The PayloadClass Metaclass registers all created instances of Payload derived classes."""

    @classmethod
    def __prepare__(metacls, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        ns = dict(namespace)
        klass = type.__new__(cls, name, bases, dict(namespace))
        if 'payload_type' in ns:
            PAYLOADS[ns['payload_type']] = klass

        return klass


class Payload(metaclass=PayloadClass):
    """Apple Configuration Profile Payload base class"""

    def __init__(self, payload_type, identifier, uuid=None, version=1, **kwargs):
        # required keys (in all payload & profile types)
        new_payload_dict = {
            'PayloadType': payload_type,
            'PayloadIdentifier': identifier,
            'PayloadUUID': uuid if uuid else str(uuid4()).upper(),
            'PayloadVersion': version,
        }

        # apply any additional argument keys to our payload
        new_payload_dict.update(kwargs)

        self.set_payload(new_payload_dict)

    def generate_dict(self):
        """Assemble a dictionary of this Payload data"""
        # avoid modifying our actual payload by using a shallow copy
        return self.payload.copy()

    def set_payload(self, payload_dict):
        """Set the internal payload dictionary and check that this payload
        is valid by having all required keys and reasonable values."""
        if 'PayloadIdentifier' not in payload_dict:
            raise PayloadKeyRequired('payload identifier is required')

        if not payload_dict['PayloadIdentifier']:
            raise PayloadValueError('payload identifier must not be empty')

        if payload_dict['PayloadIdentifier'].startswith('.'):
            raise PayloadValueError('payload identifier cannot start with a period')

        if 'PayloadType' not in payload_dict:
            raise PayloadKeyRequired('payload type is required')

        if not payload_dict['PayloadType']:
            raise PayloadValueError('payload type must not be empty')

        if 'PayloadVersion' not in payload_dict:
            raise PayloadKeyRequired('payload version is required')

        version = int(payload_dict['PayloadVersion'])

        if version < 1:
            raise PayloadValueError('payload version must be >= 1')

        payload_dict['PayloadVersion'] = version

        if 'PayloadUUID' not in payload_dict:
            raise PayloadKeyRequired('payload uuid is required')

        if not payload_dict['PayloadUUID']:
            raise PayloadValueError('payload uuid must not be empty')

        self.payload = payload_dict

    @classmethod
    def from_dict(cls, payload_dict):
        """Re-create object from dictionary"""
        if 'PayloadType' not in payload_dict:
            raise KeyError('Payload MUST contain PayloadType key')

        pldcls = find_payload_class(payload_dict['PayloadType'])

        if pldcls:
            pld = pldcls.__new__(pldcls)
        else:
            pld = Payload.__new__(Payload)

        pld.set_payload(payload_dict)
        return pld

    def get_uuid(self):
        """Returns PayloadUUID key from payload"""
        return self.payload['PayloadUUID']

    def set_uuid(self, uuid=None):
        self.payload['PayloadUUID'] = uuid if uuid else str(uuid4()).upper()
        return self.get_uuid()

    def get_identifier(self):
        return self.payload['PayloadIdentifier']

    def __repr__(self):
        if self.__class__.__name__ != Payload.__name__:
            # only show PayloadType if we're using this base class
            return '<%s ID=%r UUID=%r>' % (
                type(self).__name__, self.payload['PayloadIdentifier'], self.payload['PayloadUUID']
            )
        else:
            return '<%s Type=%r ID=%r UUID=%r>' % (
                type(self).__name__, self.payload['PayloadType'], self.payload['PayloadIdentifier'],
                self.payload['PayloadUUID'])


class Profile(Payload):
    """Apple Configuration Profile"""

    payload_type = 'Configuration'

    def __init__(self, identifier, uuid=None, version=1, **kwargs):
        Payload.__init__(self, 'Configuration', identifier, uuid, version, **kwargs)
        self.payloads = []

    def append_payload(self, payload):
        """Add a Payload to this Profile

        A Profile uses the PayloadContent key to place the aggregated Payloads
        into. Thus a Profile cannot separately set a PayloadContent key. An
        exception will be raised if this has been done."""

        if 'PayloadContent' in list(self.payload.keys()):
            raise Exception('PayloadContent already exists on Profile payload')

        self.payloads.append(payload)

    def remove_payload(self, payload):
        self.payloads.remove(payload)

    def generate_dict(self):
        """Assemble the profile dictionary including each added Payload

        A Profile uses the PayloadContent key to place the aggregated Payloads
        into. Thus a Profile cannot separately set a PayloadContent key. An
        exception will be raised if this has been done."""

        if 'PayloadContent' in list(self.payload.keys()):
            raise Exception('PayloadContent already exists on Profile payload')

        # avoid modifying our actual payload by using a shallow copy
        dict_copy = self.payload.copy()

        dict_copy['PayloadContent'] = []

        for payload in self.payloads:
            dict_copy['PayloadContent'].append(payload.generate_dict())

        return dict_copy

    @classmethod
    def from_dict(cls, payload_dict: dict):
        """Re-create object from dictionary"""

        prof = Profile.__new__(Profile)
        prof.payloads = []

        payload_dict_no_payloads = payload_dict.copy()

        if 'PayloadContent' in payload_dict_no_payloads:
            # remove any Payloads from the Profile's keys (they'll be added
            # as objects later)
            del payload_dict_no_payloads['PayloadContent']

        # give the object a payload so further functions will work
        prof.payload = payload_dict_no_payloads

        if 'PayloadContent' in payload_dict:
            for pld in payload_dict['PayloadContent']:
                # should load appropriate sub-class based on PayloadType
                new_pld = Payload.from_dict(pld)
                prof.append_payload(new_pld)

        return prof

    def generate_plist(self) -> str:
        """Generate Apple Property List XML of payload data

        Uses plistlib to generate a serialized Apple Property List XML
        representation of payload data.
        """
        return plistlib.dumps(self.generate_dict())

    @classmethod
    def from_plist(cls, plist):
        """Parse Apple Property List XML into dictionary to re-create object"""
        return cls.from_dict(plistlib.loads(plist))

    def __repr__(self):
        return '<%s ID=%r UUID=%r Payloads=%d>' % (
            self.__class__.__name__, self.payload['PayloadIdentifier'], self.payload['PayloadUUID'], len(self.payloads))

