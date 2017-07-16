from typing import Union, List
import requests
from requests.auth import AuthBase
from requests_oauthlib import OAuth1


class DEPCursor:
    pass


class DEPAuth(AuthBase):
    """Attach X-ADM-Auth-Session token to the request"""
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

    def fetch_token(self, path: str = "/session") -> Union[str, None]:
        res = self._session.get(self._url + path, auth=self._oauth)

        self._token = res.json().get("auth_session_token", None)
        return self._token

    def account(self, path: str = "/account") -> Union[None, dict]:
        res = self._session.get(self._url + path, auth=DEPAuth(self._token))
        return res.json()

    def devices(self) -> DEPCursor:
        pass

    def device_detail(self, *serial_numbers: List[str]):
        pass

    def define_profile(self, profile: dict):
        pass

    def assign_profile(self, profile_uuid: str, *serial_numbers: List[str]):
        pass

    def profile(self, uuid: str) -> dict:
        pass

    def remove_profile(self, *serial_numbers: List[str]):
        pass
