#!/usr/bin/env python
'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Flask
from commandment.scep.glue import init_libcrypto, get_libcrypto
from commandment.scep.message import SCEPAttribute
from commandment.scep.app import scep_app
from commandment.database import config_engine, init_db

import os
from cStringIO import StringIO

class WSGIChunkedBodyCopy(object):
    '''WSGI wrapper that handles chunked encoding of the request body. Copies 
    de-chunked body to a WSGI environment variable called `body_copy` (so best
    not to use with large requests lest memory issues crop up.'''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        wsgi_input = environ.get('wsgi.input')
        if 'chunked' in environ.get('HTTP_TRANSFER_ENCODING', '') and \
                environ.get('CONTENT_LENGTH', '') == '' and \
                wsgi_input:

            body = ''
            sz = int(wsgi_input.readline(), 16)
            while sz > 0:
                body += wsgi_input.read(sz + 2)[:-2]
                sz = int(wsgi_input.readline(), 16)

            environ['body_copy'] = body
            environ['wsgi.input'] = StringIO(body)

        return self.app(environ, start_response)

if __name__ == '__main__':
    app = Flask(__name__)

    app.config.from_object('commandment.default_settings')

    if os.environ.get('COMMANDMENT_SETTINGS'):
        app.config.from_envvar('COMMANDMENT_SETTINGS')

    init_libcrypto(app.config.get('LIBCRYPTO_PATH'))

    SCEPAttribute.openssl_init()

    config_engine(app.config['DATABASE_URI'], app.config['DATABASE_ECHO'])

    init_db()

    app.register_blueprint(scep_app)

    app.wsgi_app = WSGIChunkedBodyCopy(app.wsgi_app)

    app.run(
        host='0.0.0.0',
        port=app.config.get('SCEP_PORT', 5080),
        threaded=True)
