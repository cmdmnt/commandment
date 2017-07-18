from collections.abc import Iterator
from typing import Union, List
import requests
from requests.auth import AuthBase
from requests_oauthlib import OAuth1
import re
from datetime import timedelta
from .errors import DEPError


class DEPCursor(Iterator):

    def __init__(self, owner: DEP):
        self.owner = owner

    def __iter__(self):
        pass

    def __next__(self):
        pass
        


class DEPAuth(AuthBase):
    """Attach X-ADM-Auth-Session token to the request.

    Example:
          session.get("https://something", auth=DEPAuth(token))
    """
    def __init__(self, token: str):
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
                 url: str = "https://mdmenrollment.apple.com"):

        self._auth_session_token = None
        self._oauth = OAuth1(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret,
        )
        self._url = url
        self._session = requests.session()
        self._session.headers.update({
            "X-Server-Protocol-Version": "2",
            "Content-Type": "application/json;charset=UTF8",
            "User-Agent": DEP.UserAgent,
        })
        self._token = None

    def _set_token_from_header(self, r: requests.Response, *args, **kwargs):
        """This method is added as a `response` hook to the request. If the service replies with a header
        **X-ADM-Auth-Session**, then that token will replace the current token.

        Args:
              r (requests.Response): The response object

        See Also:
            - `Footnote about **X-ADM-Auth-Session** under Response Payload <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW2>`_.
        """
        if 'X-ADM-Auth-Session' in r.headers:
            self._token = r.headers['X-ADM-Auth-Session']

    def _set_retry_after(self, r: requests.Response, *args, **kwargs):
        """This method inspects the response headers for a `Retry-After` header."""
        if 'Retry-After' in r.headers:
            after = r.headers['Retry-After']
            if re.compile(r"/[0-9]+").match(after):
                d = timedelta(seconds=after)
            else:  # HTTP Date
                pass

    def send(self, req: requests.Request, **kwargs) -> requests.Response:
        """Send a request to the DEP service.

        If the service responds that the token has expired, fetch a new session token and re-issue the request.

        Args:
              req (requests.Request): The request, which will have DEP auth headers added to it.
        Returns:
              requests.Response: The response
        """
        req.hooks = dict(response=self._set_token_from_header)
        req.auth = DEPAuth(self._token)

        prepared = self._session.prepare_request(req)

        res = self._session.send(prepared, **kwargs)

        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            raise DEPError(response=res, request=res.request) from e

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
            raise DEPError(response=res, request=res.request) from e

        self._token = res.json().get("auth_session_token", None)
        return self._token

    def account(self) -> Union[None, dict]:
        """Get Account Details

        Returns:
               Union[None, dict]: The account information, or None if it failed.
        """
        res = self.send(requests.Request("GET", self._url + "/accounts"))
        return res.json()

    def devices(self, limit: int = 100, cursor: Union[str, None] = None) -> dict:
        """Fetch a list of DEP devices
        """
        req = requests.Request("POST", self._url + "/server/devices", json={'limit': limit, 'cursor': cursor})
        res = self.send(req)
        return res.json()
        

    def device_detail(self, *serial_numbers: List[str]):
        pass

    def define_profile(self, profile: dict):
        pass

    def assign_profile(self, profile_uuid: str, *serial_numbers: List[str]):
        pass

    def unassign_profile(self, *serial_numbers: List[str]):
        pass

    def profile(self, uuid: str) -> dict:
        pass

