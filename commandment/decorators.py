from typing import Union
from functools import wraps

from asn1crypto.cms import CertificateSet, SignerIdentifier
from flask import request, abort, current_app, g
from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend

import plistlib
from asn1crypto import cms


def _find_signer_sid(certificates: CertificateSet, sid: SignerIdentifier) -> Union[cms.Certificate,None]:
    """Find a signer certificate by its SignerIdentifier.
    
    Args:
          certificates (CertificateSet): Set of certificates parsed by asn1crypto.
          sid (SignerIdentifier): Signer Identifier, usually IssuerAndSerialNumber.
    Returns:
          cms.Certificate or None
    """
    if sid.name != 'issuer_and_serial_number':
        return None  # Only IssuerAndSerialNumber for now

    #: IssuerAndSerialNumber
    ias = sid.chosen

    for c in certificates:
        if c.name != 'certificate':
            continue  # we only support certificate for now

        chosen = c.chosen  #: Certificate

        if chosen.serial_number != ias['serial_number'].native:
            continue

        if chosen.issuer == ias['issuer']:
            return c
        
    return None


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


