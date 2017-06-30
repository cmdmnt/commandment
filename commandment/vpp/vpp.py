import requests
from enum import Enum
from typing import Tuple, Set, List
from collections.abc import Iterator

from commandment.vpp.errors import VPPTransportError

SERVICE_CONFIG_URL = 'https://vpp.itunes.apple.com/WebObjects/MZFinance.woa/wa/VPPServiceConfigSrv'



class VPPCursor(object):
    """Generic base class for operations on endpoints that require a token to retrieve multiple pages of records."""

    @property
    def batch_token(self) -> str:
        return ''

    @property
    def since_modified_token(self) -> str:
        return ''

    def __init__(self):
        pass


class VPPUserCursor(VPPCursor):
    pass


class VPPLicenseCursor(VPPCursor):
    pass


class LicenseAssociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'

LicenseAssociation = Tuple[LicenseAssociationType, str]


class LicenseDisassociationType(Enum):
    ClientUserID = 'ClientUserID'
    SerialNumber = 'SerialNumber'
    LicenseID = 'LicenseID'

LicenseDisassociation = Tuple[LicenseDisassociationType, str]


class VPPLicenseOperation(object):

    def __init__(self, adam_id: str, pricing_param: str = 'STDQ'):
        self._adam_id = adam_id
        self._pricing_param = pricing_param
        self._associate: List[LicenseAssociation] = []
        self._disassociate: List[LicenseDisassociation] = []

    def add(self, association_type: LicenseAssociationType, value: str):
        # TODO: Duplicate checking
        self._associate.append((association_type, value))

    def remove(self, disassociation_type: LicenseDisassociationType, value: str):
        # TODO: Duplicate checking
        self._disassociate.append((disassociation_type, value))

    def save(self):
        pass


class VPP(object):

    def __init__(self, stoken: str, vpp_service_config_url: str = SERVICE_CONFIG_URL):
        """
        The VPP class is a wrapper around a requests session and provides an API for interacting with Apple's VPP
        service.
        
        Args:
            stoken (str): Service Token
        """
        self._session = requests.Session()
        self._stoken = stoken
        
        service_config = self._fetch_config(vpp_service_config_url)
        self._service_config = service_config

    def _fetch_config(self, service_config_url: str) -> dict:
        """Fetch the service configuration from Apple, which contains all of the URLs required for VPP.

        Args:
            service_config_url (str): The VPPServiceConfigSrv URL to use
        """
        res = self._session.get(service_config_url)
        if res.status_code < 200 or res.status_code > 299:
            raise VPPTransportError('VPPServiceConfigSrv returned non 2xx status')

        return res.json()
        
    def register_user(self, user_id: str, email: str = None, facilitator_member_id: str = None,
                      managed_apple_id: str = None):
        """
        Register an MDM user with VPP.

        Args:
            user_id (str): A unique string, usually a UUID to identify the user in the MDM.
            email (str): The e-mail address of the user.
            facilitator_member_id (str):
            managed_apple_id (str):

        Returns:

        """
        pass

    def get_user(self, client_user_id: str = None, its_id: str = None, facilitator_member_id: str = None,
                 user_id: str = None):
        """
        Get the status of a user by their unique ID.
        
        Args:
            client_user_id:
            its_id:
            facilitator_member_id:
            user_id:

        Returns:

        """
        pass

    def retire_user(self, client_user_id: str = None, facilitator_member_id: str = None,
                    user_id: str = None):
        """
        Unregister a user from VPP.
        
        Args:
            client_user_id:
            facilitator_member_id:
            user_id:

        Returns:

        """
        pass

    def get_assets(self, include_license_counts: bool = True, facilitator_member_id: str = None):
        """
        Get assets for which the organization has licenses.
        
        Args:
            include_license_counts:
            facilitator_member_id:

        Returns:

        """
        pass

    def manage(self, adam_id: str, pricing_param: str = 'STDQ') -> VPPLicenseOperation:
        """Manage VPP licenses for the given Adam ID.

        Args:
            adam_id (str): The Adam ID
            pricing_param (str): The pricing param defaults to 'STDQ' but may be 'PLUS' for things which aren't
            software.

        Returns:
            VPPLicenseOperation: an instance of a VPP license operation which can be modified to add or remove devices,
            and then submitted.
        """
        op = VPPLicenseOperation(adam_id, pricing_param)
        op._vpp = self
        return op

