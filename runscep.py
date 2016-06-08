#!/usr/bin/env python
'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Flask
from commandment.scep.glue import init_libcrypto, get_libcrypto
from commandment.scep.message import SCEPMessageOID
from commandment.scep.app import scep_app

import os

if __name__ == '__main__':
    app = Flask(__name__)

    app.config.from_object('commandment.default_settings')

    if os.environ.get('COMMANDMENT_SETTINGS'):
        app.config.from_envvar('COMMANDMENT_SETTINGS')

    init_libcrypto(app.config.get('LIBCRYPTO_PATH'))

    SCEPMessageOID.openssl_init()

    app.register_blueprint(scep_app)

    app.run(
        host='0.0.0.0',
        port=app.config.get('SCEP_PORT', 5080),
        threaded=True)
