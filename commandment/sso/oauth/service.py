from typing import Optional
from flask import current_app
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.utils import request
from datetime import datetime, timedelta
from commandment.sso.models import db, OAuthClient, OAuthGrant, OAuthToken, User

oauth = OAuth2Provider()


def get_current_user():
    return User.query.first()

@oauth.clientgetter
def load_client(client_id: str) -> OAuthClient:
    return OAuthClient.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id: str, code: str) -> OAuthGrant:
    return OAuthGrant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id: str, code: str, req: request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = OAuthGrant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=req.redirect_uri,
        _scopes=' '.join(req.scopes),
        user=get_current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token: Optional[OAuthToken]=None, refresh_token: Optional[OAuthToken]=None):
    if access_token:
        return OAuthToken.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return OAuthToken.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs) -> OAuthToken:
    toks = OAuthToken.query.filter_by(client_id=request.client.client_id,
                                      user_id=request.user.id)
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = OAuthToken(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok
