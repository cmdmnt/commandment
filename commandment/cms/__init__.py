from base64 import b64encode
from typing import Union, Optional, Type, Any
from asn1crypto.cms import CertificateSet, SignerIdentifier, Certificate, SignedDigestAlgorithm, DigestAlgorithm, CMSAttributes
from asn1crypto.core import Sequence
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import current_app


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


class CMSSignedAttributeStruct(Sequence):
    _fields = [
        ('A', CMSAttributes)
    ]


def clean_cms_signed_attributes(attributes: CMSAttributes) -> bytes:
    """
    This utility removes the leading sequence octets from signed attributes
    mimics https://github.com/mozilla-services/pkcs7/blob/3a1db52591c76b9c21a6fb04c0404519b7bddfa7/sign.go#L75
    :param attributes: CMSAttributes
    :return: bytes
    """
    return CMSSignedAttributeStruct({"A": attributes})["A"].dump()


def _get_signed_attribute(attributes: CMSAttributes, attribute_name: str) -> Any:
    """
    Find and return an attribute value of type 'attribute_name' from attributes
    :param attributes: CMSAttributes Signed Attributes
    :param attribute_name: string Attribute name to look for
    :return: Any
    """
    for i in range(0, len(attributes)):
        signed_attr = attributes[i]
        if signed_attr['type'].native == attribute_name:
            return signed_attr['values'][0].native


def _verify_signature_digest(attributes: CMSAttributes, data: bytes, hash_fn: hashes.HashAlgorithm):
    """
    Computes digest of data according to 'hash_fn' and matches it with the digest in signed 'attributes'.
    :param attributes: CMSAttributes Signed Attributes
    :param data: bytes Data that is signed
    :param hash_fn: Hashes.Algorithm hash function used to compute the hash
    :return: None raise exception on signature mismatch
    """
    message_digest = _get_signed_attribute(attributes, "message_digest")
    if not message_digest:
        raise InvalidSignature("Message digest not found in signature attributes.")
    current_app.logger.debug("SignerInfo digest: %s", b64encode(message_digest))
    digest = hashes.Hash(hash_fn, default_backend())
    digest.update(data)
    computed_hash = digest.finalize()
    if computed_hash != message_digest:
        raise InvalidSignature("Siganture digest {} and Computed digest {} do not match.".format(b64encode(message_digest),
                                                                                                 b64encode(computed_hash)))


def _verify_signature_time(attributes: CMSAttributes, certificate: Certificate):
    """
    Checks the validity of signature.
    :param attributes: CMSAttributes Signed Attributes
    :param certificate: cms.Certificate
    :return: None raise exception if signature time is out of certificate validity.
    """
    signature_time = _get_signed_attribute(attributes, "signing_time")
    if signature_time is None:
        raise InvalidSignature("Signing time not found in signature attributes.")
    validity = certificate["tbs_certificate"]["validity"]
    if signature_time < validity["not_before"].native or signature_time > validity["not_after"].native:
        raise InvalidSignature("Signing time {} is outside of certificate validity {} to {}".format(signature_time,
                                                                                                    validity["not_before"].native,
                                                                                                    validity["not_after"].native))
