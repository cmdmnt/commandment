# -*- coding: utf-8 -*-
"""
Volume Purchase Programme Support
"""

import requests
from typing import List, Union, Optional, Iterator, Tuple
import json
import base64

from commandment.vpp.decorators import raise_error_replies
from commandment.vpp.enum import LicenseAssociation, LicenseDisassociation, LicenseAssociationType, \
    LicenseDisassociationType, VPPPricingParam

SERVICE_CONFIG_URL = 'https://vpp.itunes.apple.com/WebObjects/MZFinance.woa/wa/VPPServiceConfigSrv'
"""str: The default production URL to fetch VPP service configuration from."""


def encode_stoken(token: dict) -> bytes:
    """Encode a dict containing the sToken properties into a base64 token for use with VPP.

    Args:
          token (dict): Token containing the 'token', 'expDate', and 'orgName' fields.

    Returns:
          bytes: Base64 encoded token.
    """
    return base64.urlsafe_b64encode(json.dumps(token, separators=(',', ':')).encode('utf8'))


class VPPCursor(object):
    """Generic base class for operations on endpoints that require a token to retrieve multiple pages of records.

    Attributes:
          _current (dict): Current results.
          _vpp (VPP): Instance of the VPP object that generated this cursor.
    """

    @property
    def batch_count(self) -> Optional[int]:
        """Optional[int]: Number of records returned in this batch."""
        return self._current.get('batchCount', None)

    @property
    def total(self) -> Optional[int]:
        """Optional[int]: Number of records in total that will be returned."""
        return self._current.get('totalCount', None)

    @property
    def batch_token(self) -> Optional[str]:
        """Optional[str]: The batch token, if a batch fetch is in progress and is not complete."""
        return self._current.get('batchToken', None)

    @property
    def since_modified_token(self) -> Optional[str]:
        """Optional[str]: The since modified token, if a batch fetch is not in progress, but a fetch has been
        made."""
        return self._current.get('sinceModifiedToken', None)

    def __init__(self, since_modified_token: str = None, vpp=None):
        self._current = {}
        if since_modified_token is not None:
            self._current['sinceModifiedToken'] = since_modified_token

        self._vpp = vpp


class VPPUserCursor(VPPCursor):
    """VPPUserCursor represents a batch fetch operation on the `getVPPUsersSrv` endpoint.

    Attributes:
          includes_retired (bool): This fetch operation includes users that have been marked as *Retired*.
    """

    @property
    def users(self) -> Optional[List[dict]]:
        """Optional[List[dict]]: The current set of users in the cursor result, or None if there are no results."""
        return self._current.get('users', None)

    def __init__(self, includes_retired: bool = True, vpp=None):
        super(VPPUserCursor, self).__init__(vpp=vpp)
        self.includes_retired = includes_retired

    def next(self):
        """

        Returns:
            next VPPUserCursor or None when batch is exhausted
        """
        if self.batch_token is not None:
            next_cursor = self._vpp.users(batch_token=self.batch_token)
            next_cursor.includes_retired = self.includes_retired

            return next_cursor
        else:
            return None


class VPPLicenseCursor(VPPCursor):
    """VPPLicenseCursor represents a batch fetch operation on the `getVPPLicensesSrv` endpoint.

    """

    @property
    def licenses(self) -> Optional[List[dict]]:
        """Optional[List[dict]]: The current set of licenses in the cursor result, or None if there are
        no results."""
        return self._current.get('licenses', None)

    def __init__(self, *args, **kwargs):
        super(VPPLicenseCursor, self).__init__(*args, **kwargs)

    def next(self):
        """

        Returns:
            next VPPLicenseCursor or None when batch is exhausted
        """
        if self.batch_token is not None:
            next_cursor = self._vpp.licenses(batch_token=self.batch_token)
            self._current = next_cursor._current
            return self
        else:
            return None


class VPPLicenseOperation(object):
    """VPPLicenseOperation represents a number of license operations on a single Adam ID (iTunes Store Product).

    Attributes:
          _association_type (LicenseAssociationType): This specifies the type of association this license operation
            represents. The API only accepts one of these in a single request.
          _disassociation_type (LicenseDisassociationType): This specifies the type of disassociation this license
            operation represents. The API only accepts one of these in a single request.
    """

    @property
    def adam_id(self) -> int:
        return self._adam_id

    @property
    def pricing_param(self) -> str:
        return self._pricing_param

    @property
    def associations(self) -> Tuple[LicenseAssociationType, List[LicenseAssociation]]:
        return self._association_type, self._associate

    @property
    def disassociations(self) -> Tuple[LicenseDisassociationType, List[LicenseDisassociation]]:
        return self._disassociation_type, self._disassociate

    def __init__(self, adam_id: int, pricing_param: str = 'STDQ',
                 license_association_type: Optional[LicenseAssociationType] = None,
                 license_disassociation_type: Optional[LicenseDisassociationType] = None):
        self._adam_id = adam_id
        self._pricing_param = pricing_param
        self._associate: List[LicenseAssociation] = []
        self._disassociate: List[LicenseDisassociation] = []
        self._association_type = license_association_type
        self._disassociation_type = license_disassociation_type

    def add(self, association_type: LicenseAssociationType, value: str):
        if self._association_type is None:
            self._association_type = association_type
        elif association_type != self._association_type:
            raise ValueError('You cannot specify two different types of association in a license operation.')

        self._associate.append((association_type, value))

    def additions_for_type(self, association_type: LicenseAssociationType) -> Iterator[LicenseAssociation]:
        return filter(lambda x: x[0] == association_type, self._associate)

    def remove(self, disassociation_type: LicenseDisassociationType, value: str):
        if self._disassociation_type is None:
            self._disassociation_type = disassociation_type
        elif disassociation_type != self._disassociation_type:
            raise ValueError('You cannot specify two different types of disassociation in a license operation.')

        self._disassociate.append((disassociation_type, value))

    def removals_for_type(self, disassociation_type: LicenseDisassociationType) -> Iterator[LicenseDisassociation]:
        return filter(lambda x: x[0] == disassociation_type, self._disassociate)


class VPPUserLicenseOperation(VPPLicenseOperation):
    """This object represents a batch operation on a license which will be associated to or disassociated from an
    MDM user. AKA VPP User License Assignment."""

    def __init__(self, *args, **kwargs):
        super(VPPUserLicenseOperation, self).__init__(*args, **kwargs)
        self._association_type = LicenseAssociationType.ClientUserID
        self._disassociation_type = LicenseDisassociationType.ClientUserID


class VPPDeviceLicenseOperation(VPPLicenseOperation):
    """This object represents a batch operation on a license which will be associated to or disassociated from a
    Device Serial Number. AKA VPP Device License Assignment."""

    def __init__(self, *args, **kwargs):
        super(VPPDeviceLicenseOperation, self).__init__(*args, **kwargs)
        self._association_type = LicenseAssociationType.SerialNumber
        self._disassociation_type = LicenseDisassociationType.SerialNumber


class VPP(object):

    AssociationProperties = {
        LicenseAssociationType.ClientUserID: 'associateClientUserIdStrs',
        LicenseAssociationType.SerialNumber: 'associateSerialNumbers'
    }

    DisassociationProperties = {
        LicenseDisassociationType.SerialNumber: 'disassociateSerialNumbers',
        LicenseDisassociationType.ClientUserID: 'disassociateClientUserIdStrs',
        LicenseDisassociationType.LicenseID: 'disassociateLicenseIdStrs',
    }

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
        return res.json()

    @raise_error_replies
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
        return res.json()

    @raise_error_replies
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
        return res.json()

    def users(self, include_retired: int = 1, facilitator_member_id: str = None,
              batch_token: str = None, since_modified_token: str = None) -> VPPUserCursor:
        """

        Args:
            include_retired (int): 0 - do not include retired users, 1 - include retired users
            facilitator_member_id: Currently unused
            batch_token (str): Batch token (if being called from a cursor)
            since_modified_token (str): Since modified token (if requesting a time delta)

        Returns:

        """
        request_body = {'sToken': self._stoken}
        if include_retired == 1:
            request_body['includeRetired'] = 1

        if batch_token is not None:
            request_body['batchToken'] = batch_token
        elif since_modified_token is not None:
            request_body['sinceModifiedToken'] = since_modified_token

        res = self._session.post(self._service_config['getUsersSrvUrl'], data=json.dumps(request_body))
        results = res.json()
        cursor = VPPUserCursor(includes_retired=(include_retired == 1))
        cursor._current = results
        cursor._vpp = self

        return cursor

    @raise_error_replies
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
        return res.json()

    @raise_error_replies
    def edit_user(self, client_user_id: str = None, facilitator_member_id: str = None,
                  email: str = None, managed_apple_id: str = None,
                  user_id: str = None):
        """
        Edit a user's VPP record.
        
        Args:
            client_user_id (str): A unique string, usually a UUID to identify the user in the MDM. You can use this OR
                the user_id to identify the user.
            facilitator_member_id: Currently unused
            email (str): Supply an E-mail address to update the current address.
            user_id (int): User ID which uniquely identifies the user with the iTunes store.
            managed_apple_id (str): Managed Apple ID

        Returns:
            dict: Containing the reply from the service.
        """
        request_body = {'sToken': self._stoken}
        if user_id is not None:
            request_body['userId'] = user_id
        else:
            request_body['clientUserIdStr'] = client_user_id

        if email is not None:
            request_body['email'] = email

        if managed_apple_id is not None:
            request_body['managedAppleIDStr'] = managed_apple_id

        res = self._session.post(self._service_config['editUserSrvUrl'], data=json.dumps(request_body))
        return res.json()

    @raise_error_replies
    def assets(self, include_license_counts: bool = True, facilitator_member_id: str = None) -> List[dict]:
        """
        Get assets for which the organization has licenses.
        
        Args:
            include_license_counts (bool): Include counts of total/assigned/unassigned licenses.
            facilitator_member_id: Currently unused

        Returns:
            List[dict]: List of VPP assets for which this organization has licenses.
        """
        request_body = {
            'sToken': self._stoken,
            'includeLicenseCounts': include_license_counts,
        }

        res = self._session.post(self._service_config['getVPPAssetsSrvUrl'], data=json.dumps(request_body))
        return res.json()

    def manage(self, adam_id: int, pricing_param: str = 'STDQ') -> VPPLicenseOperation:
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

    def manage_user_licenses(self, adam_id: int, pricing_param: str = 'STDQ') -> VPPUserLicenseOperation:
        """Manage VPP User License Assignment.

        Args:
            adam_id (str): The Adam ID
            pricing_param (str): The pricing param defaults to 'STDQ' but may be 'PLUS' for things which aren't
            software.

        Returns:
            VPPUserLicenseOperation: an instance of a VPP license operation which can be modified to add or remove license
                associations by user client id
            """
        op = VPPUserLicenseOperation(adam_id, pricing_param)
        op._vpp = self
        return op

    def manage_device_licenses(self, adam_id: int, pricing_param: str = 'STDQ') -> VPPDeviceLicenseOperation:
        """Manage VPP Device License Assignment.

        Args:
            adam_id (str): The Adam ID
            pricing_param (str): The pricing param defaults to 'STDQ' but may be 'PLUS' for things which aren't
            software.

        Returns:
            VPPDeviceLicenseOperation: an instance of a VPP license operation which can be modified to add or remove
                license associations by device serial number
        """
        op = VPPDeviceLicenseOperation(adam_id, pricing_param)
        op._vpp = self
        return op

    def licenses(self,
                 adam_id: int = None,
                 pricing_param: Optional[VPPPricingParam] = None,
                 assigned_only: bool = False,
                 facilitator_member_id: str = None,
                 batch_token: str = None,
                 since_modified_token: str = None) -> VPPLicenseCursor:
        """Retrieve a list of licenses matching the supplied criteria.

        Args:
              adam_id (int): Get licenses that match this Adam ID
              pricing_param (Optional[VPPPricingParam]): Get licenses that match this 'Quality' param.
              assigned_only (bool): Return only licenses that are assigned to users, if this value is true.
              facilitator_member_id (str): Currently unused
              batch_token (str): Supplied if there are more results to fetch.
              since_modified_token (str): Supplied if you want to fetch results modified since a certain date. This will
                be supplied on the last page of your most recent set of results.

        Returns:
              VPPLicenseCursor: A cursor that can be used to fetch all remaining results, pre-populated with the first
                page.
        """
        request_body = {'sToken': self._stoken}
        if assigned_only:
            request_body['assignedOnly'] = True
        if batch_token:
            request_body['batchToken'] = batch_token
        if since_modified_token:
            request_body['sinceModifiedToken'] = since_modified_token

        # These parameters are normally ignored if a batch/modified token is supplied.
        if batch_token is None and since_modified_token is None:
            if adam_id is not None:
                request_body['adamId'] = adam_id
            if pricing_param is not None:
                request_body['pricingParam'] = pricing_param.value

        res = self._session.post(self._service_config['getLicensesSrvUrl'], data=json.dumps(request_body))
        reply = res.json()
        cursor = VPPLicenseCursor(vpp=self)
        cursor._current = reply

        return cursor

    def save(self, operation: VPPLicenseOperation, notify: bool = False) -> dict:
        """Execute a license management operation, represented by a VPPLicenseOperation or subclass."""
        atype, associations = operation.associations
        dtype, disassociations = operation.disassociations

        request_body = {
            'sToken': self._stoken,
            'adamIdStr': operation.adam_id,
            'pricingParam': operation.pricing_param,
            'notifyDisassociation': notify,
            VPP.AssociationProperties[atype]: associations,
            VPP.DisassociationProperties[dtype]: disassociations,
        }

        res = self._session.post(self._service_config['manageVPPLicensesByAdamIdSrvUrl'], data=json.dumps(request_body))
        reply = res.json()

        return reply

    def bulk_update_licenses(self,
                             adam_id: int,
                             association_type: Optional[LicenseAssociationType] = None,
                             associate: Optional[List[str]] = None,
                             disassociation_type: Optional[LicenseDisassociationType] = None,
                             disassociate: Optional[List[str]] = None,
                             pricing_param: str = 'STDQ',
                             notify: bool = False) -> dict:
        """Perform a batch operation of license associations and disassociations.

        Args:
              adam_id (int): Adam ID - The iTunes Store Product for which licenses will be managed.
              association_type (Optional[LicenseAssociationType]): Provide an association type if associate length > 0
              associate (Optional[List[str]]): A list of values that will be used to associate licenses, corresponding
                to the association_type
              disassociation_type (Optional[LicenseDisassociationType]): Provide a disassociation type if disassociate
                length > 0.
              disassociate (Optional[List[str]]): A list of values that will be used to disassociate licenses,
                corresponding to the association_type
              pricing_param (str): Defaults to Standard Quality 'STDQ'
              notify (bool): Notify disassociation, default is False

        See Also:
            - manageVPPLicensesByAdamIdSrv
        """
        request_body = {
            'sToken': self._stoken,
            'adamIdStr': adam_id,
            'pricingParam': pricing_param,
            'notifyDisassociation': notify,
        }

        if association_type in VPP.AssociationProperties:
            request_body[VPP.AssociationProperties[association_type]] = associate

        if disassociation_type in VPP.DisassociationProperties:
            request_body[VPP.DisassociationProperties[disassociation_type]] = disassociate

        res = self._session.post(self._service_config['manageVPPLicensesByAdamIdSrvUrl'], data=json.dumps(request_body))
        reply = res.json()

        return reply
