'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from oauthlib.oauth1 import Client
from urllib2 import Request, urlopen, HTTPError
import json

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

        response = urlopen(request, input_data).read()

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
        except HTTPError, e:
            response = e.read().strip("\"\n\r").lower()

            if e.code == 403 and response == 'forbidden':
                # authentication token is invalid
                # try to get a new one
                self.oauth1()

                # try the request a second time
                return self.api_request(api_endpoint, method, input_dict)

            if e.code == 401 and response == 'unauthorized':
                # authentication token has expired
                # try to get a new one
                self.oauth1()

                # try the request a second time
                return self.api_request(api_endpoint, method, input_dict)

            raise
