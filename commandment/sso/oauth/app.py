from flask import Blueprint, request, render_template
from commandment.sso.models import OAuthClient
from commandment.sso.oauth.service import oauth

oauth_app = Blueprint('oauth_app', __name__)


@oauth_app.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = OAuthClient.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@oauth_app.route('/token')
@oauth.token_handler
def access_token():
    return None