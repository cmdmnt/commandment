'''
JSON encoding for sending to device.
'''

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

import json
import datetime

class JSONMobileEncoder(json.JSONEncoder):
    def default(self, obj):
        '''Enhanced serialization to allow datetime in DB.'''

        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return obj
