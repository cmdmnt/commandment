#!/usr/bin/env python
'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import os
import tempfile
import atexit
import werkzeug.serving
import pkg_resources
import json
from flask.ext.redis import FlaskRedis
from flask import url_for
from commandment.app import create_app
from commandment.database import config_engine, init_db
from commandment.pki.ca import get_or_generate_web_certificate
from commandment.runner import start_runner, stop_runner
from commandment.push import push_init

if __name__ == '__main__':
    configuration = {
        'debug': False
    }

    configuration_file = pkg_resources.resource_filename(
        pkg_resources.Requirement.parse('commandment'),
        'config/config.json'
    )

    if os.path.exists(configuration_file):
        with open(configuration_file, 'r') as configuration_fh:
            loaded_configuration = json.load(configuration_fh)
        configuration.update(loaded_configuration)

    for key in ('host', 'port', 'pass', 'database'):
        keyu = key.upper()
        if os.environ.get('REDIS_%s' % keyu):
            configuration['redis'][key] = os.environ.get('REDIS_%s' % keyu)

    app = create_app(configuration['debug'], FlaskRedis(), configuration)

    if 'database' not in configuration:
        configuration['database'] = {
            'uri': app.config['DATABASE_URI'],
            'echo': app.config['DATABASE_ECHO']
        }

    if os.environ.get('COMMANDMENT_PORT'):
        configuration['port'] = int(os.environ.get('COMMANDMENT_PORT'))

    if 'port' not in configuration:
        configuration['port'] = app.config.get('PORT')

    app.logger.info(configuration)

    app.config.update(configuration)

    print configuration['database']['uri'], configuration['database']['echo']
    config_engine(configuration['database']['uri'], configuration['database']['echo'])

    init_db()

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
    os.write(cert_handle, web_crt_pem + '\n' + web_ca_pem)
    os.write(pkey_handle, web_key_pem)
    os.close(cert_handle)
    os.close(pkey_handle)

    # Werkzeug, in debug mode, will launch the app using the debug file-system
    # watching auto-reloader. For threads this means that there would be two
    # sets of threads launched. Here we try to guard against that by only
    # starting our runner threads when either the reloader (debug) is off, or
    # only in the reloader sub-process and not the reloader parent process to
    # avoid extraneous threads being created.
    if not app.config.get('DEBUG') or werkzeug.serving.is_running_from_reloader():
        start_runner()
        atexit.register(stop_runner)
        push_init()

    app.run(
        host='0.0.0.0',
        port=configuration['port'],
        ssl_context=(cert_file, pkey_file),
        threaded=True)
