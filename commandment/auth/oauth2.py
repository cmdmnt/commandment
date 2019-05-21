from authlib.flask.oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.flask.oauth2.sqla import (
    create_query_token_func,
    create_save_token_func,
    create_query_client_func,
)
from authlib.specs.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
    ImplicitGrant as _ImplicitGrant,
    ResourceOwnerPasswordCredentialsGrant as _PasswordGrant,
    ClientCredentialsGrant as _ClientCredentialsGrant,
    RefreshTokenGrant as _RefreshTokenGrant,
)
from authlib.specs.rfc7009 import RevocationEndpoint as _RevocationEndpoint
from werkzeug.security import gen_salt
from .models import (
    db, User,
    OAuth2Client,
    # OAuth2AuthorizationCode,
    OAuth2Token,
)

#
# class AuthorizationCodeGrant(_AuthorizationCodeGrant):
#     def create_authorization_code(self, client, user, request):
#         code = gen_salt(48)
#         item = OAuth2AuthorizationCode(
#             code=code,
#             client_id=client.client_id,
#             redirect_uri=request.redirect_uri,
#             scope=request.scope,
#             user_id=user.id,
#         )
#         db.session.add(item)
#         db.session.commit()
#         return code
#
#     def parse_authorization_code(self, code, client):
#         item = OAuth2AuthorizationCode.query.filter_by(
#             code=code, client_id=client.client_id).first()
#         if item and not item.is_expired():
#             return item
#
#     def delete_authorization_code(self, authorization_code):
#         db.session.delete(authorization_code)
#         db.session.commit()
#
#     def create_access_token(self, token, client, authorization_code):
#         item = OAuth2Token(
#             client_id=client.client_id,
#             user_id=authorization_code.user_id,
#             **token
#         )
#         db.session.add(item)
#         db.session.commit()
#         token['user_id'] = authorization_code.user_id


class ImplicitGrant(_ImplicitGrant):
    def create_access_token(self, token, client, grant_user):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=grant_user.id,
            **token
        )
        db.session.add(item)
        db.session.commit()


class PasswordGrant(_PasswordGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(name=username).first()
        return user
        # if user.check_password(password):
        #     return user

    def create_access_token(self, token, client, user):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=user.id,
            **token
        )
        db.session.add(item)
        db.session.commit()
        token['user_id'] = user.id


class ClientCredentialsGrant(_ClientCredentialsGrant):
    def create_access_token(self, token, client):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=client.user_id,
            **token
        )
        db.session.add(item)
        db.session.commit()


class RefreshTokenGrant(_RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.is_refresh_token_expired():
            return item

    def create_access_token(self, token, authenticated_token):
        item = OAuth2Token(
            client_id=authenticated_token.client_id,
            user_id=authenticated_token.user_id,
            **token
        )
        db.session.add(item)
        db.session.delete(authenticated_token)
        db.session.commit()


class RevocationEndpoint(_RevocationEndpoint):
    def query_token(self, token, token_type_hint, client):
        q = OAuth2Token.query.filter_by(client_id=client.client_id)
        if token_type_hint == 'access_token':
            return q.filter_by(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            return q.filter_by(refresh_token=token).first()
        # without token_type_hint
        item = q.filter_by(access_token=token).first()
        if item:
            return item
        return q.filter_by(refresh_token=token).first()

    def invalidate_token(self, token):
        db.session.delete(token)
        db.session.commit()


query_client = create_query_client_func(db.session, OAuth2Client)
save_token = create_save_token_func(db.session, OAuth2Token)
authorization = AuthorizationServer(query_client=query_client, save_token=save_token)

# support all grants
# authorization.register_grant_endpoint(AuthorizationCodeGrant)
authorization.register_grant(ImplicitGrant)
authorization.register_grant(PasswordGrant)
authorization.register_grant(ClientCredentialsGrant)
authorization.register_grant(RefreshTokenGrant)

# support revocation
# authorization.register_grant(RevocationEndpoint)

# scopes definition
scopes = {
    'email': 'Access to your email address.',
    'connects': 'Access to your connected networks.'
}

# protect resource
query_token = create_query_token_func(db.session, OAuth2Token)
require_oauth = ResourceProtector()


def init_app(app):
    authorization.init_app(app)
