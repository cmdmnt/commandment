#!/usr/bin/env python
"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

import os
import atexit
import werkzeug.serving
from commandment import create_app
from commandment.pki.ssl import generate_self_signed_certificate, generate_signing_request
from cryptography.hazmat.primitives import serialization

from commandment.apns.push import get_apns
from commandment.runner import start_runner, stop_runner

def server():
    """Run server in standalone development mode."""
    
    app = create_app(os.environ['COMMANDMENT_SETTINGS'])

    # Werkzeug, in debug mode, will launch the app using the debug file-system
    # watching auto-reloader. For threads this means that there would be two
    # sets of threads launched. Here we try to guard against that by only
    # starting our runner threads when either the reloader (debug) is off, or
    # only in the reloader sub-process and not the reloader parent process to
    # avoid extraneous threads being created.

    # TODO: re-enable runner after python3 rewrite

    with app.app_context():
        apns = get_apns()
    #
    #
    # if not app.config.get('DEBUG') or werkzeug.serving.is_running_from_reloader():
    #     start_runner()
    #     atexit.register(stop_runner)

    cert_path = os.path.join(app.root_path, app.config.get('SSL_CERTIFICATE'))
    key_path = os.path.join(app.root_path, app.config.get('SSL_RSA_KEY'))
    app.logger.debug('Using RSA Private Key From: %s', os.path.abspath(key_path))
    app.logger.debug('Using SSL Certificate From: %s', os.path.abspath(cert_path))

    # pk, csr = generate_signing_request(app.config['PUBLIC_HOSTNAME'])
    # app.logger.debug('Generated signing request for', app.config['PUBLIC_HOSTNAME'])

    if not os.path.exists(cert_path) and not os.path.exists(key_path):
        app.logger.info('Generating Self Signed Certificate')
        pk, cert = generate_self_signed_certificate(app.config['PUBLIC_HOSTNAME'])

        pem_key = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(key_path, 'wb') as fd:
            fd.write(pem_key)

        pem_cert = cert.public_bytes(
            encoding=serialization.Encoding.PEM
        )

        with open(cert_path, 'wb') as fd:
            fd.write(pem_cert)


    # http://werkzeug.pocoo.org/docs/0.11/serving/#werkzeug.serving.run_simple
    app.run(
        host='0.0.0.0',
        port=app.config.get('PORT'),
        ssl_context=(cert_path, key_path),
        threaded=True)
