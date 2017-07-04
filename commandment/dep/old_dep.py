"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from oauthlib.oauth1 import Client
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

class DEP4xxError(Exception):
    def __new__(cls, *args, **kwargs):
        '''Dynamically use the correct subclass based on the code and response
        of the exception.

        E.g. if the second argument is EXPIRED_CURSOR then instead of the
        DEP4xxError() class use the appropraite ExpiredCursor() class instead
        which will be defined in it's own subclass. Allows us to have very
        clean looking exceptions in the code without having to access
        Exception properties or special-casing Exception raising.'''
        if cls == DEP4xxError:
            for scls in cls.__subclasses__():
                if len(args) >= 1:
                    # compare our subclass code to the supplied code to find
                    # a matching subclass. default to code 400 if the subclass
                    # does not specify one.
                    if getattr(scls, 'code', 400) != args[0]:
                        continue

                if len(args) >= 2:
                    # compare our subclass body response to the supplied
                    # response to find a matching subclass. we've seen depsim
                    # use differently-cased responses so only compare
                    # lower()'d responses here
                    if getattr(scls, 'body', '').lower() != args[1].lower():
                        continue

                return scls.__new__(scls, *args, **kwargs)

        return super(DEP4xxError, cls).__new__(cls, *args, **kwargs)

    def __init__(self, code, http_body, http_exc=None, *args, **kwargs):
        super(Exception, self).__init__(code, http_body, http_exc, *args, **kwargs)

        self.code = code
        self.http_body = http_body
        self.http_exc = http_exc

class Forbidden(DEP4xxError):
    # DEP authentication token is invalid
    code = 403
    body = 'FORBIDDEN'

class Unauthorized(DEP4xxError):
    # DEP authentication token is expired
    code = 401
    body = 'UNAUTHORIZED'

class DEP(object):
    def __init__(self,
                 server_token,
                 session_token=None,
                 url_base=None,
                 new_session_callback=None,
                 user_agent='coMmanDMent/0.1'):
        self.url_base = url_base if url_base else 'https://mdmenrollment.apple.com'
        self.server_token = server_token
        self.session_token = session_token
        self.new_session_callback = new_session_callback
        self.user_agent = user_agent

    def oauth1(self):
        auth_url = self.url_base + '/session'

        oauth1_client = Client(
            self.server_token['consumer_key'],
            client_secret=self.server_token['consumer_secret'],
            resource_owner_key=self.server_token['access_token'],
            resource_owner_secret=self.server_token['access_secret'])

        uri, headers, body = oauth1_client.sign(auth_url)

        request = Request(auth_url)

        request.add_header('Authorization', headers['Authorization'])
        request.add_header('Content-Type', 'application/json;charset=UTF8')
        request.add_header('X-Server-Protocol-Version', '2')

        response = urlopen(request).read()

        # TODO: catch HTTP errors here, do something useful

        resp_dict = json.loads(response)

        self.session_token = resp_dict['auth_session_token']

        if self.new_session_callback:
            self.new_session_callback(self.session_token)

        return self.session_token

    def api_request(self, api_endpoint, method='GET', input_dict=None):
        if not api_endpoint or len(api_endpoint) < 1:
            raise Exception('DEP Web Service URL endpoint too short')

        # add beginning slash if it doesn't exist
        if not api_endpoint.startswith('/'):
            api_endpoint = '/' + api_endpoint

        request = Request(self.url_base + api_endpoint)

        request.add_header('User-Agent', self.user_agent)
        request.add_header('X-Server-Protocol-Version', '2')
        request.add_header('X-ADM-Auth-Session', self.session_token)
        request.add_header('Content-Type', 'application/json;charset=UTF8')

        if method is not 'GET':
            request.get_method = lambda: method

        input_data = json.dumps(input_dict) if input_dict else None

        try:
            response = urlopen(request, input_data).read()
        except HTTPError as e:
            # read and strip the HTTP response body
            stripped_body = e.read().strip("\"\n\r")

            if e.code in (400, 401, 403):
                raise DEP4xxError(e.code, stripped_body, e)

            raise

        resp_dict = json.loads(response)

        return resp_dict

    def auth_api_request(self, api_endpoint, method='GET', input_dict=None):
        '''Send API request to DEP or depsim providing OAuth where necessary.

        We implement the logic of attempting OAuth1 authentication here. We
        could have tried to implement recursive calling of `api_request()` but
        to avoid potential infinite loops and to more granularly control the
        flow we opted to manually code the error cases and retries here.
        '''

        # if we have no auth/session token, then try to get one
        if not self.session_token:
            self.oauth1()

        try:
            return self.api_request(api_endpoint, method, input_dict)
        except (Unauthorized, Forbidden):
            self.oauth1()
            return self.api_request(api_endpoint, method, input_dict)
