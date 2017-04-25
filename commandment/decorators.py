from typing import Union
from functools import wraps


from asn1crypto.cms import CertificateSet, SignerIdentifier
from flask import request, abort, current_app, g
from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from base64 import b64decode
import plistlib
from asn1crypto import cms
from .models import db, DeviceIdentityCertificate
from sqlalchemy.orm.exc import NoResultFound


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


def verify_mdm_signature(f):
    """Verify the signature supplied by the client in the request using the ``Mdm-Signature`` header.
    
    If the authenticity of the message has been verified,
    then the signer is attached to the **g** object as **g.signer**
    
    :reqheader Mdm-Signature: BASE64-encoded CMS Detached Signature of the message. (if `SignMessage` was true)
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'Mdm-Signature' not in request.headers:
            current_app.logger.debug('Client did not supply an Mdm-Signature header but signature is required.')
            # abort(401)

        sig = b64decode(request.headers['Mdm-Signature'])
        ci = cms.ContentInfo.load(sig)  # SignedData with zero length encap_content_info type: data
        assert ci['content_type'].native == 'signed_data'
        sd = ci['content']

        g.signer = None
        
        for si in sd['signer_infos']:
            sid = si['sid']
            signer = _find_signer_sid(sd['certificates'], sid)
            if signer is None:
                continue  # No appropriate signer found

            certificate = x509.load_der_x509_certificate(signer.dump(), default_backend())
            verifier = certificate.public_key().verifier(
                si['signature'].native,
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            verifier.update(request.data)
            verifier.verify()

            g.signer = certificate

            # TODO: I'm assuming that the device only has a single signer here

        return f(*args, **kwargs)

    return decorator


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

