"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""
from enum import Enum

PROFILE_CONTENT_TYPE = 'application/x-apple-aspen-config'


class PayloadScope(Enum):
    User = 'User'
    System = 'System'


class DeviceAttributes(Enum):
    """This enumeration describes all of the device attributes available to OTA profile enrolment."""
    UDID = 'UDID'
    VERSION = 'VERSION'
    PRODUCT = 'PRODUCT'
    SERIAL = 'SERIAL'
    MEID = 'MEID'
    IMEI = 'IMEI'
