from flask import app
from functools import wraps


class MessageRouter(object):
    """Message router routes requests by their plist ``RequestType`` attribute."""

    def __init__(self, current_app: app):
        self._app = current_app

    def route(self, message_type: str):
        
        def decorator(f):
            
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped
        return decorator

