import os
from typing import List, Union
from asn1crypto.core import PrintableString
from asn1crypto import x509 as asn1x509
from asn1crypto.cms import CMSAttribute, ContentInfo, EnvelopedData, SignedData, SignerInfos, \
    SignerInfo, CMSAttributes, SignerIdentifier, IssuerAndSerialNumber, OctetString, CertificateSet, \
    CertificateChoices, ContentType, DigestAlgorithms
from asn1crypto.algos import DigestAlgorithm, SignedDigestAlgorithm, SignedDigestAlgorithmId, DigestAlgorithmId, \
    DigestInfo

from oscrypto.keys import parse_certificate
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from .enums import MessageType, PKIStatus, FailInfo
from uuid import uuid4
from .asn1 import SCEPCMSAttributeType


CMSAttribute._fields = [
    ('type', SCEPCMSAttributeType),
    ('values', None),
]


def certificates_from_asn1(cert_set: CertificateSet) -> List[x509.Certificate]:
    """Convert an asn1crypto CertificateSet to a list of cryptography.x509.Certificate."""
    result = list()

    for cert in cert_set:
        cert_choice = cert.chosen
        assert isinstance(cert_choice, asn1x509.Certificate)  # Can't handle any other type
        result.append(x509.load_der_x509_certificate(cert_choice.dump(), default_backend()))

    return result


def create_degenerate_certificate(certificate: x509.Certificate) -> ContentInfo:
    """Produce a PKCS#7 Degenerate case with a single certificate.

    Args:
          certificate (x509.Certificate): The certificate to attach to the degenerate pkcs#7 payload.
    Returns:
          ContentInfo: The ContentInfo containing a SignedData structure.
    """
    der_bytes = certificate.public_bytes(
        serialization.Encoding.DER
    )
    asn1cert = parse_certificate(der_bytes)

    empty = ContentInfo({
        'content_type': ContentType('data')
    })
    sd = SignedData({
        'version': 1,
        'encap_content_info': empty,
        'certificates': CertificateSet([CertificateChoices('certificate', asn1cert)]),
    })

    return ContentInfo({
        'content_type': ContentType('signed_data'),
        'content': sd,
    })


class Signer(object):
    """The signer object represents a single signer on a SignedData structure.
    
    It provides a convenient way of generating a signature and a SignerInfo.
    
    Attributes:
          certificate (x509.Certificate): Signers certificate
          private_key (rsa.RSAPrivateKey): Signers private key
    """

    digest_algorithm_id = DigestAlgorithmId('sha256')
    digest_algorithm = DigestAlgorithm({'algorithm': digest_algorithm_id})
    signed_digest_algorithm_id = SignedDigestAlgorithmId('sha256_rsa')
    signed_digest_algorithm = SignedDigestAlgorithm({'algorithm': signed_digest_algorithm_id})

    def __init__(self,
                 certificate: x509.Certificate,
                 private_key: rsa.RSAPrivateKeyWithSerialization,
                 signed_attributes: List[CMSAttribute] = None):

        self.certificate = certificate
        self.private_key = private_key
        if signed_attributes is not None:
            self.signed_attributes = signed_attributes
        else:
            self.signed_attributes = []

    @property
    def sid(self) -> SignerIdentifier:
        """Get a SignerIdentifier for IssuerAndSerialNumber"""
        derp = self.certificate.public_bytes(serialization.Encoding.DER)
        asn1cert = parse_certificate(derp)

        # Signer Identifier
        ias = IssuerAndSerialNumber({'issuer': asn1cert.issuer, 'serial_number': asn1cert.serial_number})
        sid = SignerIdentifier('issuer_and_serial_number', ias)
        return sid

    def sign(self, data: bytes, content_type: ContentType, content_digest: bytes, cms_attributes: List[CMSAttribute]) -> SignerInfo:
        """Generate a signature encrypted with the signer's private key and return the SignerInfo."""
        # The CMS standard requires that the content-type authenticatedAttribute and the message-digest
        # attribute must be present if any authenticatedAttribute exist at all.
        self.signed_attributes = cms_attributes

        self.signed_attributes.insert(0, CMSAttribute({
            'type': 'message_digest',
            'values': [OctetString(content_digest)],
        }))

        self.signed_attributes.insert(0, CMSAttribute({
            'type': 'content_type',
            'values': [ContentType('data')],
        }))

        cms_attributes = CMSAttributes(self.signed_attributes)

        # Calculate Digest
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(cms_attributes.dump())
        d = digest.finalize()

        # Make DigestInfo from result
        digest_info = DigestInfo({
            'digest_algorithm': self.digest_algorithm,
            'digest': d,
        })

        # Get the RSA key to sign the digestinfo
        signer = self.private_key.signer(
            asympad.PKCS1v15(),
            hashes.SHA256()
        )

        signer.update(cms_attributes.dump())
        signature = signer.finalize()

        signer_info = SignerInfo({
            'version': 1,
            'sid': self.sid,
            'digest_algorithm': self.digest_algorithm,
            'signed_attrs': cms_attributes,

            # Referred to as ``digestEncryptionAlgorithm`` in the RFC
            'signature_algorithm': self.signed_digest_algorithm,

            # Referred to as ``encryptedDigest`` in the RFC
            'signature': OctetString(signature),
        })

        return signer_info


class PKIMessageBuilder(object):
    """The PKIMessageBuilder builds pkiMessages as defined in the SCEP RFC.

    Attributes:
          _signers: List of signers to create signatures and populate signerinfos.
          _cms_attributes: List of CMSAttribute
          _certificates: List of Certificates
          _pki_envelope: The enveloped data being signed

    See Also:
          - `<https://tools.ietf.org/html/draft-nourse-scep-23#section-3.1>`_.
    """

    def __init__(self):
        self._signers = []
        self._cms_attributes = []
        self._certificates = None
        self._pki_envelope = None

    def certificates(self, *certificates: List[x509.Certificate]):
        """Add x.509 certificates to be attached to the certificates field.

        Args:
              certificates: variadic argument of x509.Certificate
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `pkcs#7 RFC 2315 Section 9.1 <https://tools.ietf.org/html/rfc2315#section-9.1>`_.
        """
        certset = CertificateSet()

        for cert in certificates:
            # Serialize and load to avoid constructing asn1crypto.Certificate ourselves (yuck)
            derp = cert.public_bytes(serialization.Encoding.DER)
            asn1cert = parse_certificate(derp)
            choice = CertificateChoices('certificate', asn1cert)
            certset.append(choice)

        self._certificates = certset

        return self

    def add_signer(self, signer: Signer):
        """Add a signer to SignerInfos.

        Args:
              signer (Signer): Signer instance
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `pkcs#7 RFC2315 Section 9.2 <https://tools.ietf.org/html/rfc2315#section-9.2>`_.
        """
        self._signers.append(signer)

        return self

    def message_type(self, message_type: MessageType):
        """Set the SCEP Message Type Attribute.

        Args:
              message_type (MessageType): A valid PKIMessage messageType
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.2.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        attr = CMSAttribute({
            'type': 'message_type',
            'values': [PrintableString(message_type.value)],
        })
        self._cms_attributes.append(attr)

        return self

    def pki_envelope(self, envelope: EnvelopedData):
        """Set content for encryption inside the pkcsPKIEnvelope

        Args:
            envelope (EnvelopedData): The pkcsPKIEnvelope

        Returns:
            PKIMessageBuilder: This instance
        """
        self._pki_envelope = envelope
        
        return self

    def pki_status(self, status: PKIStatus, failure_info: FailInfo = None):
        """Set the PKI status of the operation.

        Args:
              status (PKIStatus): A valid pkiStatus value
              failure_info (FailInfo): A failure info type, which must be present if PKIStatus is failure.
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.3.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        attr = CMSAttribute({
            'type': 'pki_status',
            'values': [PrintableString(status.value)],
        })
        self._cms_attributes.append(attr)

        if status == PKIStatus.FAILURE:
            if failure_info is None:
                raise ValueError('You cannot specify failure without failure info')

            fail_attr = CMSAttribute({
                'type': 'fail_info',
                'values': [PrintableString(failure_info.value)],
            })
            self._cms_attributes.append(fail_attr)

        return self

    def sender_nonce(self, nonce: Union[bytes, OctetString] = None):
        """Add a sender nonce.

        Args:
              nonce (bytes or OctetString): Sender nonce
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.5.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        if isinstance(nonce, bytes):
            nonce = OctetString(nonce)
        elif nonce is None:
            nonce = OctetString(os.urandom(16))

        attr = CMSAttribute({
            'type': 'sender_nonce',
            'values': [nonce],
        })

        self._cms_attributes.append(attr)
        return self

    def recipient_nonce(self, nonce: Union[bytes, OctetString]):
        """Add a recipient nonce.

        Args:
              nonce (bytes or OctetString): Recipient nonce
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.5.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        if isinstance(nonce, bytes):
            nonce = OctetString(nonce)

        attr = CMSAttribute({
            'type': 'recipient_nonce',
            'values': [nonce],
        })

        self._cms_attributes.append(attr)
        return self

    def transaction_id(self, trans_id: Union[str, PrintableString] = None):
        """Add a transaction ID.

        Args:
              trans_id (str or PrintableString): Transaction ID. If omitted, one is generated
        Returns:
              PKIMessageBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.1.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        if isinstance(trans_id, str):
            trans_id = PrintableString(trans_id)
        elif trans_id is None:
            trans_id = PrintableString(str(uuid4()))

        attr = CMSAttribute({
            'type': 'transaction_id',
            'values': [trans_id]
        })

        self._cms_attributes.append(attr)
        return self

    def _build_cmsattributes(self) -> CMSAttributes:
        """Finalize the set of CMS Attributes and return the collection.

        Returns:
              CMSAttributes: All of the added CMS attributes
        """
        return CMSAttributes(value=self._cms_attributes)

    def _build_signerinfos(self, content: bytes, content_digest: bytes, cms_attributes: List[CMSAttribute]) -> SignerInfos:
        """Build all signer infos and return a collection.

        Returns:
            SignerInfos: all signers
        """
        return SignerInfos(signer.sign(content, ContentType('data'), content_digest, cms_attributes) for signer in self._signers)

    def finalize(self) -> ContentInfo:
        """Build all data structures from the given parameters and return the top level contentInfo.

        Returns:
              ContentInfo: The PKIMessage
        """
        pkcs_pki_envelope = self._pki_envelope
        encap_info = ContentInfo({
            'content_type': ContentType('data'),
            'content': pkcs_pki_envelope.dump(),
        })

        # Calculate digest on encrypted content + signed_attrs
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(pkcs_pki_envelope.dump())
        d = digest.finalize()
        
        # Now start building SignedData

        signer_infos = self._build_signerinfos(pkcs_pki_envelope.dump(), d, self._cms_attributes)

        certificates = self._certificates

        da_id = DigestAlgorithmId('sha256')
        da = DigestAlgorithm({'algorithm': da_id})
        das = DigestAlgorithms([da])

        sd = SignedData({
            'version': 1,
            'certificates': certificates,
            'signer_infos': signer_infos,
            'digest_algorithms': das,
            'encap_content_info': encap_info,
        })

        ci = ContentInfo({
            'content_type': ContentType('signed_data'),
            'content': sd,
        })

        return ci

