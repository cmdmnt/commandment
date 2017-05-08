import os
from flask import current_app, g
from flask_oauthlib.client import OAuth, OAuthRemoteApp
from base64 import b64encode

oauth = OAuth()


def google():
    current_app.logger.debug('getting google oauth provider')
    google = oauth.remote_app('google',
                              consumer_key=current_app.config['GOOGLE_CONSUMER_KEY'],
                              consumer_secret=current_app.config['GOOGLE_CONSUMER_SECRET'],
                              request_token_url=None,
                              access_token_url='https://www.googleapis.com/oauth2/v4/token',
                              authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
                              request_token_params={
                                  'scope': 'email profile',
#                                  'state': lambda: b64encode(os.urandom(10))
                              }
                              )
    return google


def get_oauth() -> OAuthRemoteApp:
    provider = getattr(g, '_oauth', None)
    if provider is None:
        provider = g._oauth = google()
    return provider
