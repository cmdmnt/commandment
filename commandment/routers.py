from flask import app, Blueprint, request, abort
from functools import wraps
import biplist
from .models import db, Command, CommandStatus
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class CommandRouter(object):
    """Command router routes mdm client requests by the type of command that is being responded to.
    
    It sets up a view function on the specified route, usually the MDM endpoint, and responds to PUT requests.
    If the request content isn't plist, you will receive a HTTP Status 400 Bad Request.
    
    Args:
          app (app): The flask application or blueprint instance
          url (str): The HTTP(S) route that will be used as the endpoint for this plist router.
    """
    def __init__(self, app: app, url: str):
        self._app = app
        app.add_url_rule(url, view_func=self.view, methods=['PUT'])
        self.request_types = {}

    def view(self):
        try:
            plist_data = biplist.readPlistFromString(request.data)
        except biplist.NotBinaryPlistException:
            abort(400, 'The request body does not contain a plist as expected')
        except biplist.InvalidPlistException:
            abort(400, 'The request body does not contain a valid plist')

        if 'CommandUUID' not in plist_data:
            abort(400, 'The request body does not contain a Command UUID to process')

        try:
            command = db.session.query(Command).filter(Command.uuid == plist_data['CommandUUID']).one()
        except NoResultFound:
            abort(400, 'The device responded with a command UUID that does not exist')
        except MultipleResultsFound:
            abort(500, 'There were multiple matching commands, this should never happen')

        if command.command_class in self.request_types:
            for handler in self.request_types[command.command_class]:  # just return first handler for now
                return handler(command, plist_data)

    def route(self, request_type: str):
        """
        Route a plist request by its RequestType key value.
        
        The wrapped function must accept (command, plist_data)
        
        :param request_type: 
        :return: 
        """

        if request_type not in self.request_types:
            self.request_types[request_type] = []

        handlers = self.request_types[request_type]

        def decorator(f):
            handlers.append(f)

            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped
        return decorator



class PlistRouter(object):
    """PlistRouter routes requests to view functions based on matching values to top level keys.
    
    """
    def __init__(self, app: app, url: str):
        self._app = app
        app.add_url_rule(url, view_func=self.view, methods=['PUT'])
        self.kv_routes = []

    def view(self):
        try:
            plist_data = biplist.readPlistFromString(request.data)
        except biplist.NotBinaryPlistException:
            abort(400, 'The request body does not contain a plist as expected')
        except biplist.InvalidPlistException:
            abort(400, 'The request body does not contain a valid plist')

        for kvr in self.kv_routes:
            if kvr['key'] not in plist_data:
                continue

            if plist_data[kvr['key']] == kvr['value']:
                return kvr['handler'](plist_data)

        abort(404, 'No matching plist route')

    def route(self, key: str, value: any):
        """
        Route a plist request if the content satisfies the key value test
        
        The wrapped function must accept (plist_data)
        """
        def decorator(f):
            self.kv_routes.append(dict(
                key=key,
                value=value,
                handler=f
            ))

            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped
        return decorator
