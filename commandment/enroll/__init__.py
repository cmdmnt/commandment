from enum import Enum


class DeviceAttributes(Enum):
    """This enumeration describes all of the device attributes available to OTA profile enrolment.
    """
    UDID = 'UDID'
    VERSION = 'VERSION'
    PRODUCT = 'PRODUCT'
    SERIAL = 'SERIAL'
    MEID = 'MEID'
    IMEI = 'IMEI'


AllDeviceAttributes = {DeviceAttributes.UDID.value, DeviceAttributes.VERSION.value, DeviceAttributes.PRODUCT.value,
                       DeviceAttributes.SERIAL.value, DeviceAttributes.MEID.value, DeviceAttributes.IMEI.value}

