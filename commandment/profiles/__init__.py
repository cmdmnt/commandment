'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

'''Support for Apple Configuration Profiles and Payloads'''

import plistlib
from uuid import uuid4

class Payload(object):
    '''Apple Configuration Profile Payload base class'''
    def __init__(self, payload_type, identifier, uuid=None, version=1, **kwargs):
        if not identifier:
            raise ValueError('payload identifier is required')

        if identifier.startswith('.'):
            raise ValueError('payload identifier cannot start with a period')

        if not payload_type:
            raise ValueError('payload type is required')

        version = int(version)

        if version < 1:
            raise ValueError('payload version must be >= 1')

        # required keys (in all payload & profile types)
        self.payload = {
            'PayloadType': payload_type,
            'PayloadIdentifier': identifier,
            'PayloadUUID': uuid if uuid else str(uuid4()).upper(),
            'PayloadVersion': version,
        }

        # remove any required fields from the optional supplied keys
        for kwkey in self.payload.keys():
            if kwkey in kwargs:
                del kwargs[kwkey]

        # apply any additional argument keys to our payload
        self.payload.update(kwargs)

    def generate_dict(self):
        '''Assemble a dictionary of this Payload data'''
        # avoid modifying our actual payload by using a shallow copy
        return self.payload.copy()

    @classmethod
    def from_dict(cls, payload_dict):
        '''Re-create object from dictionary'''
        if 'PayloadType' not in payload_dict:
            raise KeyError('Payload MUST contain PayloadType key')

        pldcls = find_payload_class(payload_dict['PayloadType'])

        if pldcls:
            pld = pldcls.__new__(pldcls)
        else:
            pld = Payload.__new__(Payload)

        pld.payload = payload_dict
        return pld

    def get_uuid(self):
        '''Returns PayloadUUID key from payload'''
        return self.payload['PayloadUUID']

    def set_uuid(self, uuid=None):
        self.payload['PayloadUUID'] = uuid if uuid else str(uuid4()).upper()
        return self.get_uuid()

    def get_identifier(self):
        return self.payload['PayloadIdentifier']

    def __repr__(self):
        if self.__class__.__name__ != Payload.__name__:
            # only show PayloadType if we're using this base class
            return '<%s ID=%r UUID=%r>' % (self.__class__.__name__, self.payload['PayloadIdentifier'], self.payload['PayloadUUID'])
        else:
            return '<%s Type=%r ID=%r UUID=%r>' % (self.__class__.__name__, self.payload['PayloadType'], self.payload['PayloadIdentifier'], self.payload['PayloadUUID'])

def find_payload_class(payload_type):
    '''Iterate through inherited classes to find a matching class name'''
    subclasses = set()
    work = [Payload]
    while work:
        parent_subclass = work.pop()
        for child_subclass in parent_subclass.__subclasses__():
            if child_subclass not in subclasses:
                if hasattr(child_subclass, 'payload_type') and child_subclass.payload_type == payload_type:
                    return child_subclass

                subclasses.add(child_subclass)
                work.append(child_subclass)

    return None


class Profile(Payload):
    '''Apple Configuration Profile'''
    def __init__(self, identifier, uuid=None, version=1, **kwargs):
        Payload.__init__(self, 'Configuration', identifier, uuid, version, **kwargs)
        self.payloads = []

    def append_payload(self, payload):
        '''Add a Payload to this Profile

        A Profile uses the PayloadContent key to place the aggregated Payloads
        into. Thus a Profile cannot separately set a PayloadContent key. An
        exception will be raised if this has been done.'''

        if 'PayloadContent' in self.payload.keys():
            raise Exception('PayloadContent already exists on Profile payload')

        self.payloads.append(payload)

    def remove_payload(self, payload):
        self.payloads.remove(payload)

    def generate_dict(self):
        '''Assemble the profile dictionary including each added Payload

        A Profile uses the PayloadContent key to place the aggregated Payloads
        into. Thus a Profile cannot separately set a PayloadContent key. An
        exception will be raised if this has been done.'''

        if 'PayloadContent' in self.payload.keys():
            raise Exception('PayloadContent already exists on Profile payload')

        # avoid modifying our actual payload by using a shallow copy
        dict_copy = self.payload.copy()

        dict_copy['PayloadContent'] = []

        for payload in self.payloads:
            dict_copy['PayloadContent'].append(payload.generate_dict())

        return dict_copy

    @classmethod
    def from_dict(cls, payload_dict):
        '''Re-create object from dictionary'''

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

    def generate_plist(self):
        '''Generate Apple Property List XML of payload data

        Uses plistlib to generate a serialized Apple Property List XML
        representation of payload data.
        '''
        return plistlib.writePlistToString(self.generate_dict())

    @classmethod
    def from_plist(cls, plist):
        '''Parse Apple Property List XML into dictionary to re-create object'''
        return cls.from_dict(plistlib.readPlistFromString(plist))

    def __repr__(self):
        return '<%s ID=%r UUID=%r Payloads=%d>' % (self.__class__.__name__, self.payload['PayloadIdentifier'], self.payload['PayloadUUID'], len(self.payloads))
