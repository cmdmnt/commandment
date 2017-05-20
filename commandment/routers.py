from typing import Union
from flask import Flask, app, Blueprint, request, abort, current_app
from functools import wraps
import biplist
from .models import db, Device
from .mdm import commands


class CommandRouter(object):
    """The command router passes off commands to handlers which are registered by RequestType.
    
    When a reply is received from a device in relation to a specific CommandUUID, the router attempts to find a handler
     that was registered for the RequestType associated with that command. The handler is then called with the specific
     instance of the command that generated the response, and an instance of the device that is making the request to
     the MDM endpoint.
    
    Args:
          app (app): The flask application or blueprint instance
    """
    def __init__(self, app: Union[Flask, Blueprint]):
        self._app = app
        self._handlers = {}

    def handle(self, command: commands.Command, device: Device, response: dict):
        if command.request_type in self._handlers:
            return self._handlers[command.request_type](command, device, response)
        else:
            current_app.logger.warning('No handler found to process command response: {}'.format(command.request_type))
            return None

    def route(self, request_type: str):
        """
        Route a plist request by its RequestType key value.
        
        The wrapped function must accept (command, plist_data)
        
        :param request_type: 
        :return: 
        """
        handlers = self._handlers
        # current_app.logger.debug('Registering command handler for request type: {}'.format(request_type))

        def decorator(f):
            handlers[request_type] = f

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
