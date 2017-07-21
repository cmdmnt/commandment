from typing import List

from asn1crypto.cms import CMSAttribute
from cryptography.exceptions import InvalidSignature
from flask import request, g, current_app, abort
from functools import wraps
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from asn1crypto import cms
from base64 import b64decode, b64encode
from . import _certificate_by_signer_identifier, _cryptography_hash_function, _cryptography_pad_function


def _verify_cms_signers(signed_data: bytes, detached: bool = False) -> (List[x509.Certificate], bytes):
    ci = cms.ContentInfo.load(signed_data)
    assert ci['content_type'].native == 'signed_data'
    signed: cms.SignedData = ci['content']

    current_app.logger.debug("CMS request contains %d certificate(s)", len(signed['certificates']))

    signers = []
    for signer in signed['signer_infos']:
        asn_certificate = _certificate_by_signer_identifier(signed['certificates'], signer['sid'])
        assert asn_certificate is not None
        certificate = x509.load_der_x509_certificate(asn_certificate.dump(), default_backend())

        digest_algorithm = signer['digest_algorithm']
        signature_algorithm = signer['signature_algorithm']

        hash_function = _cryptography_hash_function(digest_algorithm)
        pad_function = _cryptography_pad_function(signature_algorithm)

        if hash_function is None or pad_function is None:
            raise ValueError('Unsupported signature algorithm: {}'.format(signature_algorithm))
        else:
            current_app.logger.debug("Using signature algorithm: %s", signature_algorithm.native)

        assert signed['encap_content_info']['content_type'].native == 'data'

        if detached:
            data = request.data
        else:
            data = signed['encap_content_info']['content'].native

        if 'signed_attrs' in signer and len(signer['signed_attrs']) > 0:
            for i in range(0, len(signer['signed_attrs'])):
                signed_attr: CMSAttribute = signer['signed_attrs'][i]

                if signed_attr['type'].native == "message_digest":
                    current_app.logger.debug("SignerInfo digest: %s", b64encode(signed_attr['values'][0].native))

            certificate.public_key().verify(
                signer['signature'].native,
                signer['signed_attrs'].dump(),
                pad_function(),
                hash_function()
            )
        else:  # No signed attributes means we are only validating the digest
            certificate.public_key().verify(
                signer['signature'].native,
                data,
                pad_function(),
                hash_function()
            )

        signers.append(certificate)

    # TODO: Don't assume that content is OctetString

    if detached:
        return signers, request.data
    else:
        return signers, signed['encap_content_info']['content']


def verify_cms_signers(f):
    """Verify the signers of a request containing a CMS/PKCS#7, DER encoded body.

    The certificate of each signer is placed on the global **g** variable as **g.signers**

    Raises:
          - TypeError if *Content-Type* header is not "application/pkcs7-signature"
          - SigningError if any signer on the CMS content is not valid.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.testing:
            return f(*args, **kwargs)
    
        if request.headers['Content-Type'] != "application/pkcs7-signature":
            raise TypeError("verify_cms_signers expects application/pkcs7-signature, got: {}".format(
                request.headers['Content-Type']))

        g.signers, g.signed_data = _verify_cms_signers(request.data)

        return f(*args, **kwargs)

    return decorator


def verify_cms_signers_header(f):
    """Verify the signature supplied by the client in the request using the ``Mdm-Signature`` header.

    If the authenticity of the message has been verified,
    then the signer is attached to the **g** object as **g.signer**

    In unit tests, this decorator is completely disabled by the presence of testing = True

    :reqheader Mdm-Signature: BASE64-encoded CMS Detached Signature of the message. (if `SignMessage` was true)
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.testing:
            return f(*args, **kwargs)

        if 'Mdm-Signature' not in request.headers:
            raise TypeError('Client did not supply an Mdm-Signature header but signature is required.')

        detached_signature = b64decode(request.headers['Mdm-Signature'])

        try:
            signers, signed_data = _verify_cms_signers(detached_signature, detached=True)
        except InvalidSignature as e:
            current_app.logger.warn("Invalid Signature in Mdm-Signature header")
            return abort(403)

        g.signers = signers
        g.signed_data = signed_data

        return f(*args, **kwargs)

    return decorator
