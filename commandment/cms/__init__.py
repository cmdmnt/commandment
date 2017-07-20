from typing import Union, Optional, Type
from asn1crypto.cms import CertificateSet, SignerIdentifier, Certificate, SignedDigestAlgorithm, DigestAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def _certificate_by_signer_identifier(certificates: CertificateSet, sid: SignerIdentifier) -> Optional[Certificate]:
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
            return chosen

    return None


def _cryptography_hash_function(algorithm: DigestAlgorithm) -> Union[None, Type[hashes.SHA1], Type[hashes.SHA256], Type[hashes.SHA512]]:
    """Find the cryptography hash function given the string output from asn1crypto SignedDigestAlgorithm.

    Todo: There should be a better way to do this?

    Args:
          algorithm (DigestAlgorithm): The asn1crypto Signed Digest Algorithm
    Returns:
        Union[Type[hashes.SHA1], Type[hashes.SHA256], Type[hashes.SHA512]] A cryptography hash function for use with
         signature verification.
    """

    hash_algo = algorithm['algorithm'].native

    if hash_algo == "sha1":
        return hashes.SHA1
    elif hash_algo == "sha256":
        return hashes.SHA256
    elif hash_algo == "sha512":
        return hashes.SHA512
    else:
        return None


def _cryptography_pad_function(algorithm: SignedDigestAlgorithm) -> Union[None, Type[padding.PKCS1v15]]:
    """Find the cryptography pad function given a signed digest algorithm from asn1crypto.

    Args:
        algorithm (SignedDigestAlgorithm): The asn1crypto Signed Digest Algorithm
    Returns:
        Union[None, Type[padding.PKCS1v15]]: The padding function for the signed digest
        """
    signature_algo = algorithm.signature_algo

    if signature_algo == "rsassa_pkcs1v15":
        return padding.PKCS1v15
    else:
        return None
