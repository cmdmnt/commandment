from collections.abc import Iterator
from typing import Union, List, Optional
import requests
from requests.auth import AuthBase
from requests_oauthlib import OAuth1
import re
from datetime import timedelta, datetime
from dateutil import parser as dateparser
from locale import atof
import json
import logging

from commandment.dep import DEPProfileRemovals
from .errors import DEPServiceError, DEPClientError
from email.utils import parsedate  # Necessary for HTTP-Date

logger = logging.getLogger(__name__)


class DEPAuth(AuthBase):
    """Attach X-ADM-Auth-Session token to the request.

    Example:
          session.get("https://something", auth=DEPAuth(token))
    """
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r):
        r.headers['X-ADM-Auth-Session'] = self.token
        return r


class DEP:

    UserAgent = 'commandment'

    def __init__(self,
                 consumer_key: str = None,
                 consumer_secret: str = None,
                 access_token: str = None,
                 access_secret: str = None,
                 access_token_expiry: Optional[str] = None,
                 url: str = "https://mdmenrollment.apple.com") -> None:

        self._session_token: Optional[str] = None
        self._oauth = OAuth1(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret,
        )

        if access_token_expiry is not None:
            access_token_expiry_date = dateparser.parse(access_token_expiry)
            self._access_token_expiry = access_token_expiry_date
        else:
            self._access_token_expiry = None

        self._url = url
        self._session = requests.session()
        self._session.headers.update({
            "X-Server-Protocol-Version": "3",
            "Content-Type": "application/json;charset=UTF8",
            "User-Agent": DEP.UserAgent,
        })
        self._retry_after: Optional[datetime] = None

    @property
    def session_token(self) -> Optional[str]:
        return self._session_token

    @classmethod
    def from_token(cls, token: str):  # (str) -> DEP
        """Instantiate the DEP client instance from a string holding the service token json content."""
        stoken = json.loads(token)
        return cls(**stoken)

    def _response_hook(self, r: requests.Response, *args, **kwargs):
        """This method always exists as a response hook in order to keep some of the state returned by the
        DEP service internally such as:
            - The last value of the `X-ADM-Auth-Session` header, which is used on subsequent requests.
            - The last value of the `Retry-After` header, which is used to set an instance variable to indicate
                when we may make another request.

        See Also:
            - `Footnote about **X-ADM-Auth-Session** under Response Payload <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW2>`_.
        """
        if r.status_code == 401:  # Token may be expired, or token is invalid
            pass  # TODO: Need token refresh as decorator

        # If the service gives us another session token, that replaces our current token.
        if 'X-ADM-Auth-Session' in r.headers:
            self._session_token = r.headers['X-ADM-Auth-Session']

        # If the service wants to rate limit us, store that information locally.
        if 'Retry-After' in r.headers:
            after = r.headers['Retry-After']
            if re.compile(r"/[0-9]+/").match(after):
                d = timedelta(seconds=atof(after))
                self._retry_after = datetime.utcnow() + d
            else:  # HTTP Date
                self._retry_after = datetime(*parsedate(after)[:6])

    def send(self, req: requests.Request, **kwargs) -> Optional[requests.Response]:
        """Send a request to the DEP service.

        If the service responds that the token has expired, fetch a new session token and re-issue the request.

        Args:
              req (requests.Request): The request, which will have DEP auth headers added to it.
        Returns:
              requests.Response: The response
        """
        if self._access_token_expiry is not None and datetime.now() > self._access_token_expiry:
            raise DEPClientError("DEP Service Token has expired, please generate a new one.")

        if self._retry_after is not None:  # refuse to send request
            return None

        if self.session_token is None:
            self.fetch_token()

        req.hooks = dict(response=self._response_hook)
        req.auth = DEPAuth(self._session_token)

        prepared = self._session.prepare_request(req)

        res = self._session.send(prepared, **kwargs)

        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            raise DEPServiceError(response=res, request=res.request) from e

        return res

    def fetch_token(self) -> Union[str, None]:
        """Request a new session token using our DEP credentials.

        Returns:
              Union[str, None]: The token that was returned (already set on this instance), or None if it failed.
        """
        res = self._session.get(self._url + "/session", auth=self._oauth)
        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            raise DEPServiceError(response=res, request=res.request) from e

        self._session_token = res.json().get("auth_session_token", None)
        return self._session_token

    def account(self) -> Union[None, dict]:
        """Get Account Details

        The details are returned in the following dict format::

            {
                'server_name': 'MDM Server Name entered in the portal',
                'server_uuid': '<32 char UUID without separators>',
                'facilitator_id': 'E-mail of facilitator',
                'admin_id': 'Administrator E-mail Address',
                'org_name': 'Organization Name',
                'org_email': 'Organization E-mail',
                'org_phone': 'Organization Contact Phone',
                'org_address': 'Organization Physical Address'
            }

        Returns:
               Union[None, dict]: The account information, or None if it failed.
        """
        logger.debug("Fetching DEP account information")
        res = self.send(requests.Request("GET", self._url + "/account"))
        return res.json()

    def fetch_devices(self, cursor: Union[str, None] = None, limit: int = 100) -> dict:
        """Fetch a list of DEP devices

        Args:
              cursor (str): The cursor from the last fetch (must be younger than 7 days).
              limit (int): Limit the number of records in the response. Default is 100
        Returns:
              dict: Response as per the sync devices documentation.
        """
        req = requests.Request("POST", self._url + "/server/devices", json={'limit': limit, 'cursor': cursor})
        res = self.send(req)
        return res.json()

    def sync_devices(self, cursor: str, limit: int = 100) -> dict:
        """Fetch devices changed since the cursor was issued.

        Args:
              cursor (str): The cursor from the last sync (must be younger than 7 days).
              limit (int): Limit the number of records in the response. Default is 100
        Returns:
              dict: Response as per the sync devices documentation.
        """
        req = requests.Request("POST", self._url + "/devices/sync", json={'limit': limit, 'cursor': cursor})
        res = self.send(req)
        return res.json()

    def devices(self, cursor: Union[str, None] = None) -> Iterator:
        """Get an iterable object which calls fetch or sync to retrieve all device records.

        Args:
              cursor (str): If supplied, the cursor returned will perform the sync operation. Otherwise you will
                receive a cursor that performs a fetch for each iteration, until the fetch cursor is exhausted.

        Returns:
              Union[DEPSyncCursor, DEPFetchCursor]: A cursor that is iterable
        """
        if cursor is not None:
            return DEPSyncCursor(self, cursor)
        else:
            return DEPFetchCursor(self)

    def device_detail(self, *serial_numbers: Union[str, List[str]]):
        """Fetch detail about a list of devices

        Args:
              serial_numbers (List[str]): A list of device serial numbers to fetch details for.

        Returns:
              dict: Device information
        """
        req = requests.Request("POST", self._url + "/devices", json={'devices': serial_numbers})
        res = self.send(req)
        return res.json()

    def define_profile(self, profile: dict):
        """Define a DEP profile

        Args:
              profile (dict): A DEP profile.

        """
        req = requests.Request("POST", self._url + "/profile", json=profile)
        res = self.send(req)
        return res.json()

    def assign_profile(self, profile_uuid: str, *serial_numbers: List[str]) -> dict:
        """Assign an existing profile to device(s)

        Args:
              profile_uuid (str): The UUID of the profile to assign.
              serial_numbers (List[str]): A list of serial numbers to assign to that profile.

        Returns:
              dict: Assignment information
        """
        req = requests.Request("POST", self._url + "/profile/devices",
                               json={'profile_uuid': profile_uuid, 'devices': serial_numbers})
        res = self.send(req)
        return res.json()

    def remove_profile(self, *serial_numbers: List[str]) -> DEPProfileRemovals:
        """Unassign all profiles from device(s)

        Args:
              serial_numbers (List[str]): A list of serial numbers to unassign from that profile.

        Returns:
              dict: Assignment information
        """
        req = requests.Request("DELETE", self._url + "/profile/devices",
                               json={'devices': serial_numbers})
        res = self.send(req)
        return res.json()

    def profile(self, uuid: str) -> dict:
        """Get an existing profile by its UUID.

        Args:
              uuid (str): Profile UUID

        Returns:
              dict: Profile
        """
        params = {'profile_uuid': uuid} if uuid is not None else None
        req = requests.Request("GET", self._url + "/profile", params=params)
        res = self.send(req)
        return res.json()

    def activation_lock(self, serial_number: str,
                        escrow_key: Union[str, None] = None,
                        lost_message: Union[str, None] = None):
        pass

    def disown(self, *serial_numbers: List[str]):
        """Disown devices.

        This action is PERMANENT (except in the case of iPads added via Apple Configurator 2).
        """
        pass


class DEPBaseCursor(object):
    """DEPCursor is the base class for DEP Fetch and Sync cursors.

    Attributes:
          owner (DEP): The DEP instance that created this iterator.
          results (dict): The current response results.
    """

    def __init__(self, owner: DEP, results: Optional[dict] = None) -> None:
        self.owner = owner
        self.results = results

    @property
    def cursor(self) -> Optional[str]:
        if not self.results:
            return None
        return self.results.get('cursor', None)

    @property
    def more_to_follow(self) -> bool:
        if not self.results:
            return True
        return self.results.get('more_to_follow', False)

    def __iter__(self):
        return self


class DEPFetchCursor(DEPBaseCursor, Iterator):
    """DEPFetchCursor wraps the DEP device fetch cursor as an iterable object."""
    def __next__(self):
        if not self.more_to_follow:
            raise StopIteration()

        if self.cursor is None:
            self.results = self.owner.fetch_devices()
        else:
            self.results = self.owner.fetch_devices(cursor=self.cursor)

        return self.results


class DEPSyncCursor(DEPBaseCursor, Iterator):
    """DEPSyncCursor wraps the DEP device sync cursor as an iterable object."""
    def __init__(self, owner: DEP, cursor: str, results: Optional[dict] = None) -> None:
        super(DEPSyncCursor, self).__init__(owner, results)

    def __next__(self):
        if not self.more_to_follow:
            raise StopIteration()

        self.results = self.owner.fetch_devices(cursor=self.cursor)

        return self.results
