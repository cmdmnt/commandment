from typing import Tuple
from enum import Enum, IntEnum


class VPPPricingParam(Enum):
    """Valid values for the VPP pricingParam argument."""
    
    StandardQuality = 'STDQ'
    """str: Standard Quality"""
    HighQuality = 'PLUS'
    """str: High Quality - Does not apply to Software"""


class VPPUserStatus(Enum):
    """Valid values for the status of a VPP registered user."""

    Registered = 'Registered'
    """str: Registered"""
    Associated = 'Associated'
    """str: Associated"""
    Retired = 'Retired'
    """str: Retired (can still be changed back)"""
    Deleted = 'Deleted'
    """str: Deleted"""


AdamID = str
PricingParam = str
VPPAsset = Tuple[AdamID, PricingParam]
"""VPPAsset: A tuple representing a pair of product adam id and pricing parameter."""

class LicenseAssociationType(Enum):
    """Valid types of license association operations which are mutually exclusive in a single batch."""

    ClientUserID = 'ClientUserID'
    """str: Associate user to license by Client ID"""
    SerialNumber = 'SerialNumber'
    """str: Associate device to license by Serial Number"""

LicenseAssociation = Tuple[LicenseAssociationType, AdamID]
"""LicenseAssociation: A tuple representing a combination of a product by adam id and a type of association operation"""

class LicenseDisassociationType(Enum):
    """Valid types of license disassociation operations which are mutually exclusive in a single batch."""

    ClientUserID = 'ClientUserID'
    """str: Disassociate license from user by Client ID"""
    SerialNumber = 'SerialNumber'
    """str: Disassociate license from device by Serial Number"""
    LicenseID = 'LicenseID'
    """str: Disassociate license by ID regardless of User/Device"""

LicenseDisassociation = Tuple[LicenseDisassociationType, AdamID]
"""LicenseDisassociation: A tuple representing a combination of a product by adam id and a type of 
    disassociation operation"""


class VPPProductType(IntEnum):
    """A VPP product type. Required by some of the VPP API"""
    Software = 7
    """int: An piece of software"""
    Application = 8
    """int: Don't ask me"""
    Publication = 10
    """int: An ebook"""
