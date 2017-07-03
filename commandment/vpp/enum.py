from typing import Tuple
from enum import Enum


class VPPPricingParam(Enum):
    StandardQuality = 'STDQ'
    HighQuality = 'PLUS'


class VPPUserStatus(Enum):
    Registered = 'Registered'
    Associated = 'Associated'
    Retired = 'Retired'
    Deleted = 'Deleted'


AdamID = str


class LicenseAssociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'

LicenseAssociation = Tuple[LicenseAssociationType, AdamID]


class LicenseDisassociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'
    LicenseID = 'LicenseID'

LicenseDisassociation = Tuple[LicenseDisassociationType, AdamID]

