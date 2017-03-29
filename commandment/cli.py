#!/usr/bin/env python
"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

import os
import tempfile
import atexit
import werkzeug.serving
from commandment.app import create_app
from commandment.database import config_engine, init_db
from commandment.pki.certificateauthority import get_or_generate_web_certificate
from commandment.runner import start_runner, stop_runner
from commandment.push import push_init

def server():
    app = create_app()

    app.config.from_object('commandment.default_settings')

    if os.environ.get('COMMANDMENT_SETTINGS'):
        app.config.from_envvar('COMMANDMENT_SETTINGS')

    config_engine(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_DATABASE_ECHO'])

    init_db()
    with app.app_context():
        web_crt_pem, web_key_pem, web_ca_pem = get_or_generate_web_certificate(app.config['DEV_WEB_CERT_CN'])

    # Werkzeug 0.10 decided to move away from a pyOpenSSL context in favor of
    # a Python 2.7.9+/3.x+ ssl.SSLContext. This sucks because there is no API
    # to provide in-memory certificates and private keys to said context.
    # Which means we must, unfortunately, use the filesystem to store
    # certificates just so we can load them for the development web server
    # while it runs. Also, of course, OS X shipped versions of Python do not
    # have a new enough version to make use of the SSLContext directly.
    # Luckily for us Werkzeug provides it's own emulation of an SSLContext if
    # we supply the cert and pk filenames in a tuple to it's ssl_context
    # parameter. Note this is also done in push.py as the apns library uses
    # similar context objects.

    cert_handle, cert_file = tempfile.mkstemp()
    pkey_handle, pkey_file = tempfile.mkstemp()
    atexit.register(os.remove, pkey_file)
    atexit.register(os.remove, cert_file)
    os.write(cert_handle, web_crt_pem) # + '\n' + web_ca_pem
    os.write(pkey_handle, web_key_pem)
    os.close(cert_handle)
    os.close(pkey_handle)

    # Werkzeug, in debug mode, will launch the app using the debug file-system
    # watching auto-reloader. For threads this means that there would be two
    # sets of threads launched. Here we try to guard against that by only
    # starting our runner threads when either the reloader (debug) is off, or
    # only in the reloader sub-process and not the reloader parent process to
    # avoid extraneous threads being created.

    # TODO: re-enable runner after python3 rewrite
    # if not app.config.get('DEBUG') or werkzeug.serving.is_running_from_reloader():
    #     start_runner()
    #     atexit.register(stop_runner)
    #     push_init()

    app.run(
        host='0.0.0.0',
        port=app.config.get('PORT'),
        ssl_context=(cert_file, pkey_file),
        threaded=True)
