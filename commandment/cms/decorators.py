from flask import request, g, current_app
from functools import wraps
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from asn1crypto import cms
from base64 import b64decode
from . import _certificate_by_signer_identifier, _cryptography_hash_function, _cryptography_pad_function


def verify_cms_signers(f):
    """Verify the signers of a request containing a CMS/PKCS#7, DER encoded body.

    The certificate of each signer is placed on the global **g** variable as **g.signers**

    Raises:
          - TypeError if *Content-Type* header is not "application/pkcs7-signature"
          - SigningError if any signer on the CMS content is not valid.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if request.headers['Content-Type'] != "application/pkcs7-signature":
            raise TypeError("verify_cms_signers expects application/pkcs7-signature, got: {}".format(
                request.headers['Content-Type']))

        ci = cms.ContentInfo.load(request.data)
        assert ci['content_type'].native == 'signed_data'
        signed: cms.SignedData = ci['content']

        g.signers = []

        for signer in signed['signer_infos']:
            asn_certificate = _certificate_by_signer_identifier(signed['certificates'], signer['sid'])
            assert asn_certificate is not None
            certificate = x509.load_der_x509_certificate(signer.dump(), default_backend())

            signature_algorithm = signer['signature_algorithm']
            hash_function = _cryptography_hash_function(signature_algorithm)
            pad_function = _cryptography_pad_function(signature_algorithm)
            if hash_function is None or pad_function is None:
                raise ValueError('Unsupported signature algorithm: {}'.format(signature_algorithm))

            verifier = certificate.public_key().verifier(
                signer['signature'].native,
                pad_function(),
                hash_function()
            )
            verifier.update(request.data)
            verifier.verify()  # Raises a SigningError if not valid
            g.signers.append(certificate)

        # TODO: Don't assume that content is OctetString
        g.signed_data = signed['encap_content_info']['content']

        return f(*args, **kwargs)

    return decorator


def verify_mdm_signature(f):
    """Verify the signature supplied by the client in the request using the ``Mdm-Signature`` header.

    If the authenticity of the message has been verified,
    then the signer is attached to the **g** object as **g.signer**

    In unit tests, this decorator is completely disabled by the presence of testing = True

    TODO: merge with verify_cms_signers

    :reqheader Mdm-Signature: BASE64-encoded CMS Detached Signature of the message. (if `SignMessage` was true)
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.testing:
            return f(*args, **kwargs)

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
            signer = _certificate_by_signer_identifier(sd['certificates'], sid)
            if signer is None:
                continue  # No appropriate signer found

            signature_algorithm = signer['signature_algorithm']
            hash_function = _cryptography_hash_function(signature_algorithm)
            pad_function = _cryptography_pad_function(signature_algorithm)

            certificate = x509.load_der_x509_certificate(signer.dump(), default_backend())
            verifier = certificate.public_key().verifier(
                si['signature'].native,
                pad_function(),
                hash_function()
            )
            verifier.update(request.data)
            verifier.verify()  # Raises a SigningError if not valid

            g.signer = certificate

            # TODO: I'm assuming that the device only has a single signer here

        return f(*args, **kwargs)

    return decorator