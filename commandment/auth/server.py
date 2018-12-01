from authlib.flask.oauth2 import AuthorizationServer
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func
)

query_client = create_query_client_func(db.session, Client)
save_token = create_save_token_func(db.session, Token)

server = AuthorizationServer()
