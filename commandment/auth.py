'''
Copyright (c) 2017 Vladimir Panteleev
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

# from functools import wraps
from flask import request, Response, current_app

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    auth = (current_app.config['ADMIN_USERNAME'], current_app.config['ADMIN_PASSWORD'])
    return (username, password) == auth

def need_auth():
    """Return true if authentication is required."""
    return current_app.config['ADMIN_PASSWORD'] != ''

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Unauthorized', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def require_auth():
    """Called from before_request to require authentication."""
    if need_auth():
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
