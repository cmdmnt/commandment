from functools import wraps

from flask import request, abort, current_app, g
from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend

import plistlib


def parse_plist_input_data(f):
    """Parses plist data as HTTP input from request.

    The unserialized data is attached to the global **g** object as **g.plist_data**.

    :status 400: If invalid plist data was supplied in the request.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if current_app.debug:
                current_app.logger.debug(request.data)
            g.plist_data = plistlib.loads(request.data)
        except:
            current_app.logger.info('could not parse property list input data')
            abort(400, 'invalid input data')

        return f(*args, **kwargs)

    return decorator


def pem_certificate_upload(f):
    """Parse PEM formatted certificate in request data
    
    TODO: form field name option
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            certificate_data = request.files['file'].read()
            g.certificate = x509.load_pem_x509_certificate(certificate_data, backend=default_backend())
        except UnsupportedAlgorithm as e:
            current_app.logger.info('could not parse PEM certificate data')
            abort(400, 'invalid input data')

        return f(*args, **kwargs)

    return decorator


