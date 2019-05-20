from flask import Blueprint, current_app, redirect, url_for, request, flash, render_template
from authlib.flask.oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from .models import db, Client, Token, User

oauth_app = Blueprint('oauth_app', __name__)


def query_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


def save_token(token, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        user_id = None
    item = Token(
        client_id=request.client.client_id,
        user_id=user_id,
        **token
    )
    db.session.add(item)
    db.session.commit()


# or with the helper
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func
)
query_client = create_query_client_func(db.session, Client)
save_token = create_save_token_func(db.session, Token)

server = AuthorizationServer()


# This is quite insecure but we are testing at this stage.
class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        return user
        # if user.check_password(password):
        #     return user


server.register_grant(grants.ImplicitGrant)
server.register_grant(PasswordGrant)

# @oauth_app.route('/oauth/authorize', methods=['GET', 'POST'])
# def authorize():
#     # Login is required since we need to know the current resource owner.
#     # It can be done with a redirection to the login page, or a login
#     # form on this authorization page.
#     if request.method == 'GET':
#         grant = server.validate_consent_request(end_user=current_user)
#         return render_template(
#             'authorize.html',
#             grant=grant,
#             user=current_user,
#         )
#     confirmed = request.form['confirm']
#     if confirmed:
#         # granted by resource owner
#         return server.create_authorization_response(current_user)
#     # denied by resource owner
#     return server.create_authorization_response(None)


@oauth_app.route('/oauth/token', methods=['POST'])
def issue_token():
    return server.create_token_response()

