from flask import current_app
from flask_jwt import JWT, jwt_required, current_identity


def authenticate(email: str, password: str):
    return None


def identity(payload):
    current_app.logger.debug(payload)
