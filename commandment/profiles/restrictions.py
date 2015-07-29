'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from . import Payload

class RestrictionsPayload(Payload):
    payload_type = 'com.apple.applicationaccess'

    def __init__(self, identifier, uuid=None, **kwargs):
        Payload.__init__(self, self.payload_type, identifier, uuid, **kwargs)
