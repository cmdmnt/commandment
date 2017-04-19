from enum import Enum


class WIFIEncryptionType(Enum):
    ENone = 'None'
    Any = 'Any'
    WPA2 = 'WPA2'
    WPA = 'WPA'
    WEP = 'WEP'


class WIFIProxyType(Enum):
    ENone = 'None'
    Manual = 'Manual'
    Auto = 'Auto'

