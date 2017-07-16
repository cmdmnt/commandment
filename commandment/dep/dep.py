from typing import Union, List
from requests_oauthlib import OAuth1Session

class DEPCursor:
    pass


class DEP:

    UserAgent = 'commandment'

    def __init__(self,
                 consumer_key: str = None,
                 consumer_secret: str = None,
                 access_token: str = None,
                 access_secret: str = None,
                 url: str = "https://mdmenrollment.apple.com"):

        self._auth_session_token = None
        self._dep = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret,
        )
        self._url = url

    def fetch_token(self, path: str = "/session"):
        token = self._dep.fetch_request_token("{}{}".format(self._url, path))


    def account(self, path: str = "/account") -> Union[None, dict]:
        pass

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
