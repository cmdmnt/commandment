from enum import Enum


class DeviceAttributes(Enum):
    """This enumeration describes all of the device attributes available to OTA profile enrolment.
    """
    UDID = 'UDID'
    VERSION = 'VERSION'
    PRODUCT = 'PRODUCT'
    DEVICE_NAME = 'DEVICE_NAME'
    SERIAL = 'SERIAL'
    MODEL = 'MODEL'
    MAC_ADDRESS_EN0 = 'MAC_ADDRESS_EN0'
    MEID = 'MEID'
    IMEI = 'IMEI'
    ICCID = 'ICCID'
    COMPROMISED = 'COMPROMISED'
    DeviceID = 'DeviceID'
#    SPIROM = 'SPIROM'
#    MLB = 'MLB'


AllDeviceAttributes = {
    DeviceAttributes.UDID.value,
    DeviceAttributes.VERSION.value,
    DeviceAttributes.PRODUCT.value,
    DeviceAttributes.DEVICE_NAME.value,
    DeviceAttributes.SERIAL.value,
    DeviceAttributes.MODEL.value,
    # DeviceAttributes.MAC_ADDRESS_EN0.value,
    DeviceAttributes.MEID.value,
    DeviceAttributes.IMEI.value,
    DeviceAttributes.ICCID.value,
    DeviceAttributes.COMPROMISED.value,
    DeviceAttributes.DeviceID.value,
#    DeviceAttributes.SPIROM.value,
#    DeviceAttributes.MLB.value,
}

