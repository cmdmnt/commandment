import requests
from enum import Enum
from typing import Tuple, Set, List
from collections.abc import Iterator
import json
import base64

from commandment.vpp.errors import VPPTransportError, VPPTokenInvalid

SERVICE_CONFIG_URL = 'https://vpp.itunes.apple.com/WebObjects/MZFinance.woa/wa/VPPServiceConfigSrv'


def encode_stoken(token: dict) -> bytes:
    """Encode a dict containing the sToken properties into a base64 token for use with VPP.

    Args:
          token (dict): Token containing the 'token', 'expDate', and 'orgName' fields.

    Returns:
          bytes: Base64 encoded token.
    """
    return base64.urlsafe_b64encode(json.dumps(token, separators=(',', ':')).encode('utf8'))


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

    def __init__(self, stoken: str, vpp_service_config_url: str = SERVICE_CONFIG_URL, service_config: dict = None):
        """
        The VPP class is a wrapper around a requests session and provides an API for interacting with Apple's VPP
        service.
        
        Args:
            stoken (str): Service Token
            vpp_service_config_url (str): URL to the VPPServiceConfigSrv endpoint. defaults to Apple's live server.
            service_config (dict): Dictionary containing service config, if you do not want to fetch it (testing only).
        """
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})
        self._stoken = stoken

        if not service_config:
            fetched_service_config = self._fetch_config(vpp_service_config_url)
            self._service_config = fetched_service_config
        else:
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
        
    def register_user(self, client_user_id: str, email: str = None, facilitator_member_id: str = None,
                      managed_apple_id: str = None):
        """
        Register an MDM user with VPP.

        Args:
            client_user_id (str): A unique string, usually a UUID to identify the user in the MDM.
            email (str): The e-mail address of the user.
            facilitator_member_id (str): Currently unused
            managed_apple_id (str): Currently unused

        Returns:
            dict: Containing the decoded body of the reply from the VPP service, eg::

                        { "status": 0,
                            "user": {
                              "userId": 2878111686099947,
                              "email": "vpp-test@localhost",
                              "status": "Registered",
                              "inviteUrl": "http://localhost:8080/D1971F9DD5F8E67BDD",
                              "inviteCode": "D1971F9DD5F8E67BDD",
                              "clientUserIdStr": "F33D9E0F-CDE3-427E-A444-B137BEF9EFA2"
                            }
                        }
        """
        res = self._session.post(self._service_config['registerUserSrvUrl'], data=json.dumps({
            'clientUserIdStr': client_user_id,
            'email': email,
            'sToken': self._stoken,
        }))
        
        if res.status_code < 200 or res.status_code > 299:
            raise VPPTransportError('registerVPPUserSrv returned non 2xx status')

        reply = res.json()
        
        if 'status' in reply and reply['status'] == -1:  # VPP Error occurred
            raise VPPTokenInvalid('{} ({})'.format(reply['errorMessage'], reply['errorNumber']))

        return reply
        
    def get_user(self, client_user_id: str = None, its_id_hash: str = None, facilitator_member_id: str = None,
                 user_id: int = None):
        """
        Get the status of a user by their unique ID.
        
        Args:
            client_user_id (str): A unique string, usually a UUID to identify the user in the MDM. You can use this OR
                the user_id to identify the user.
            its_id_hash (str): (Optional) iTunes Store ID hash
            facilitator_member_id:
            user_id (int): User ID which uniquely identifies the user with the iTunes store.

        Returns:
            dict: Containing the reply from the service.
        """
        request_body = {'sToken': self._stoken}
        if user_id is not None:
            request_body['userId'] = user_id
        else:
            request_body['clientUserIdStr'] = client_user_id
            if its_id_hash is not None:
                request_body['itsIdHash'] = its_id_hash

        res = self._session.post(self._service_config['getUserSrvUrl'], data=json.dumps(request_body))

        if res.status_code < 200 or res.status_code > 299:
            raise VPPTransportError('getUserSrvUrl returned non 2xx status')

        reply = res.json()

        if 'status' in reply and reply['status'] == -1:  # VPP Error occurred
            raise VPPTokenInvalid('{} ({})'.format(reply['errorMessage'], reply['errorNumber']))

        return reply

    def retire_user(self, client_user_id: str = None, facilitator_member_id: str = None,
                    user_id: str = None):
        """
        Unregister a user from VPP.
        
        Args:
            client_user_id (str): A unique string, usually a UUID to identify the user in the MDM. You can use this OR
                the user_id to identify the user.
            facilitator_member_id: Currently unused
            user_id (int): User ID which uniquely identifies the user with the iTunes store.

        Returns:
            dict: Containing the reply from the service.
        """
        request_body = {'sToken': self._stoken}
        if user_id is not None:
            request_body['userId'] = user_id
        else:
            request_body['clientUserIdStr'] = client_user_id

        res = self._session.post(self._service_config['retireUserSrvUrl'], data=json.dumps(request_body))

        if res.status_code < 200 or res.status_code > 299:
            raise VPPTransportError('getUserSrvUrl returned non 2xx status')

        reply = res.json()

        if 'status' in reply and reply['status'] == -1:  # VPP Error occurred
            raise VPPTokenInvalid('{} ({})'.format(reply['errorMessage'], reply['errorNumber']))

        return reply

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

