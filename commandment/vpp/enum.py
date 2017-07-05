from typing import Tuple
from enum import Enum, IntEnum


class VPPPricingParam(Enum):
    StandardQuality = 'STDQ'
    HighQuality = 'PLUS'


class VPPUserStatus(Enum):
    Registered = 'Registered'
    Associated = 'Associated'
    Retired = 'Retired'
    Deleted = 'Deleted'


AdamID = int
PricingParam = str
VPPAsset = Tuple[AdamID, PricingParam]


class LicenseAssociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'

LicenseAssociation = Tuple[LicenseAssociationType, AdamID]


class LicenseDisassociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'
    LicenseID = 'LicenseID'

LicenseDisassociation = Tuple[LicenseDisassociationType, AdamID]


class VPPProductType(IntEnum):
    Software = 7
    Application = 8
    Publication = 10
