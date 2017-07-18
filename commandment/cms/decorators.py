from flask import request, g
from functools import wraps
from cryptography import x509
from cryptography.exceptions import UnsupportedAlgorithm, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from asn1crypto import cms
from . import _certificate_by_signer_identifier


def verify_cms_signers(f):
    """Verify the signers of a request containing a CMS/PKCS#7, DER encoded body.

    """
    @wraps(f)
    def decorator(*args, **kwargs):
        assert request.headers['Content-Type'] == "application/pkcs7-signature"

        ci = cms.ContentInfo.load(request.data)
        assert ci['content_type'].native == 'signed_data'
        signed: cms.SignedData = ci['content']

        g.signers = []

        for signer in signed['signer_infos']:
            asn_certificate = _certificate_by_signer_identifier(signed['certificates'], signer['sid'])
            assert asn_certificate is not None
            certificate = x509.load_der_x509_certificate(signer.dump(), default_backend())
            signature_algorithm = signer['signature_algorithm']
            signature_algo = signature_algorithm.signature_algo
            hash_algo = signature_algorithm.hash_algo

            hash_function = {
                'sha1': hashes.SHA1,
                'sha256': hashes.SHA256,
                'sha512': hashes.SHA512
            }.get(hash_algo, hashes.SHA1)

            pad_function = {
                'rsassa_pkcs1v15': padding.PKCS1v15
            }.get(signature_algo, padding.PKCS1v15)

            verifier = certificate.public_key().verifier(
                signer['signature'].native,
                pad_function(),
                hash_function()
            )
            verifier.update(request.data)
            verifier.verify()  # Raises a SigningError if not valid
            g.signers.append(certificate)

        return f(*args, **kwargs)

    return decorator
