from flask import Blueprint, request, url_for
from .applications import google, oauth, get_oauth

oauth_app = Blueprint('oauth_app', __name__)
oauth.init_app(oauth_app)


@oauth_app.route('/login')
def login():
    provider = get_oauth()
    return provider.authorize(callback=url_for('oauth_app.authorize', _external=True))


@oauth_app.route('/authorize')
def authorize():
    provider = get_oauth()
    resp = provider.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
