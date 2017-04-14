from typing import Union, List
import os
from .ca import CertificateAuthority
from asn1crypto.core import Integer, PrintableString
from asn1crypto.cms import CMSAttribute, ContentInfo, EnvelopedData, EncapsulatedContentInfo, SignedData, SignerInfos, \
    SignerInfo, CMSAttributes, SignerIdentifier, IssuerAndSerialNumber, Integer, OctetString, CertificateSet, \
    CertificateChoices, ContentType, ParsableOctetString, CMSVersion, DigestAlgorithms
from asn1crypto.algos import DigestAlgorithm, SignedDigestAlgorithm, SignedDigestAlgorithmId, DigestAlgorithmId, \
    DigestInfo
from oscrypto.keys import parse_certificate
from commandment.scep import asn1
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.backends import default_backend
from enum import Enum, IntEnum

CMSAttribute._fields = [
    ('type', asn1.SCEPCMSAttributeType),
    ('values', None),
]


class MessageType(Enum):
    """The SCEP Message Type.
    
    This is encoded as PrintableString so this enum also uses strings.
    
    See Also:
        - `SCEP RFC <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_ Section 3.2.1.2.
    """
    CertRep = '3'
    """Response to certificate or CRL request"""

    RenewalReq = '17'
    """PKCS #10 certificate request for renewal of
      an existing certificate."""

    UpdateReq = '18'
    """PKCS #10 certificate request for update of a
      certificate issued by a different CA."""

    PKCSReq = '19'
    """PKCS #10 certificate request."""

    CertPoll = '20'
    """Certificate polling in manual enrolment."""

    GetCert = '21'
    """Retrieve a certificate."""

    GetCRL = '22'
    """Retrieve a CRL."""


class PKIStatus(Enum):
    """The SCEP PKI Status
    
    Decimal value as printableString
    
    See Also:
        - SCEP RFC Section 3.2.1.3.
    """
    SUCCESS = '0'
    FAILURE = '2'
    PENDING = '3'


class FailInfo(Enum):
    """SCEP Failure Information"""
    BadAlg = '0'
    """Unrecognized or unsupported algorithm."""

    BadMessageCheck = '1'
    """Integrity check (meaning signature
      verification of the CMS message) failed."""

    BadRequest = '2'
    """Transaction not permitted or supported."""

    BadTime = '3'
    """The signingTime attribute from the CMS
      authenticatedAttributes was not sufficiently close to the system
      time (this failure code is present for legacy reasons and is
      unlikely to be encountered in practice)."""

    BadCertId = '4'
    """No certificate could be identified matching the
      provided criteria."""


class SignedDataBuilder(object):
    """The SignedDataBuilder builds SignedData objects in the style of cryptography.x509s fluent builder interfaces.

    Attributes:
          _signers: List of signers to create signatures and populate signerinfos.
          _primary_signer: This is the only signer that counts right now.
          _primary_signer_key (rsa.RSAPrivateKey): Signer private key
          _cms_attributes: List of CMSAttribute
          _certificates: List of Certificates
    """

    def __init__(self, signer_cert: x509.Certificate, signer_key: rsa.RSAPrivateKeyWithSerialization):
        self._signers = []
        self._primary_signer = None
        self._primary_signer_key = None

        self._cms_attributes = []
        self._certificates = None
        self.add_signer(signer_cert, signer_key)

    def certificates(self, *certificates: List[x509.Certificate]):
        """Add x.509 certificates to be attached to the certificates field.

        Args:
              certificates: variadic argument of x509.Certificate
        Returns:
              SignedDataBuilder: This instance
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

    def add_signer(self, certificate: x509.Certificate, signer_key: rsa.RSAPrivateKeyWithSerialization):
        """Add a signer to SignerInfos.

        Args:
              certificate (x509.Certificate): Signer certificate
              signer_key (rsa.RSAPrivateKeyWithSerialization): Signer RSA private key
        Returns:
              SignedDataBuilder: This instance
        See Also:
              - `pkcs#7 RFC2315 Section 9.2 <https://tools.ietf.org/html/rfc2315#section-9.2>`_.
        """
        derp = certificate.public_bytes(serialization.Encoding.DER)
        asn1cert = parse_certificate(derp)

        # Signer Identifier
        ias = IssuerAndSerialNumber({'issuer': asn1cert.issuer, 'serial_number': asn1cert.serial_number})
        sid = SignerIdentifier('issuer_and_serial_number', ias)

        self._signers.append({'sid': sid, 'certificate': certificate})
        self._primary_signer = {
            'sid': sid,
            'certificate': certificate,
        }
        self._primary_signer_key = signer_key

        return self

    def message_type(self, message_type: MessageType):
        """Set the SCEP Message Type Attribute.

        Args:
              message_type (MessageType): A valid PKIMessage messageType
        Returns:
              SignedDataBuilder: This instance
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

    def pki_status(self, status: PKIStatus, failure_info: FailInfo = None):
        """Set the PKI status of the operation.

        Args:
              status (PKIStatus): A valid pkiStatus value
              failure_info (FailInfo): A failure info type, which must be present if PKIStatus is failure.
        Returns:
              SignedDataBuilder: This instance
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

    def sender_nonce(self, nonce: Union[bytes, OctetString]):
        """Add a sender nonce.

        Args:
              nonce (bytes or OctetString): Sender nonce
        Returns:
              SignedDataBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.5.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        if isinstance(nonce, bytes):
            nonce = OctetString(nonce)

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
              SignedDataBuilder: This instance
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

    def transaction_id(self, trans_id: Union[str, PrintableString]):
        """Add a transaction ID.

        Args:
              trans_id (str or PrintableString): Transaction ID.
        Returns:
              SignedDataBuilder: This instance
        See Also:
              - `draft-gutmann-scep Section 3.2.1.1.
                <https://datatracker.ietf.org/doc/draft-gutmann-scep/?include_text=1>`_.
        """
        if isinstance(trans_id, str):
            trans_id = PrintableString(trans_id)

        attr = CMSAttribute({
            'type': 'transaction_id',
            'values': [trans_id]
        })

        self._cms_attributes.append(attr)
        return self

    def _build_cmsattributes(self) -> CMSAttributes:
        return CMSAttributes(value=self._cms_attributes)

    def _build_signerinfo(self) -> SignerInfo:
        # Add Required CMSAttributes
        self._cms_attributes.append(CMSAttribute({
            'type': 'content_type',
            'values': [ContentType('data')],
        }))

        # self._cms_attributes.append(CMSAttribute({
        #     'type': 'message_digest',
        #     'values': [],
        # }))


        # Get CMSAttributes
        unsigned_attrs = self._build_cmsattributes()
        # Calculate Digest
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(unsigned_attrs.dump())
        d = digest.finalize()
        # Make DigestInfo from result
        da_id = DigestAlgorithmId('sha256')
        da = DigestAlgorithm({'algorithm': da_id})
        di = DigestInfo({
            'digest_algorithm': da,
            'digest': d,
        })

        # Get the RSA key to sign the digestinfo
        pk = self._primary_signer_key
        signer = pk.signer(
            asympad.PKCS1v15(),
            hashes.SHA256()
        )

        signer.update(di.dump())
        signature = signer.finalize()

        sda_id = SignedDigestAlgorithmId('sha256_rsa')
        sda = SignedDigestAlgorithm({'algorithm': sda_id})

        si = SignerInfo({
            'version': CMSVersion(1),
            'sid': self._primary_signer['sid'],
            'digest_algorithm': da,
            'unsigned_attrs': unsigned_attrs,
            'signature_algorithm': sda,
            'signature': OctetString(signature),
        })
        return si

    def _build_signerinfos(self) -> SignerInfos:
        return SignerInfos([self._build_signerinfo()])

    def signed_data(self) -> SignedData:
        """Sign and return the SignedData structure."""
        signer_infos = self._build_signerinfos()
        certificates = self._certificates

        da_id = DigestAlgorithmId('sha256')
        da = DigestAlgorithm({'algorithm': da_id})
        das = DigestAlgorithms([da])

        encap_info = ContentInfo({
            'content_type': ContentType('data'),
        })

        sd = SignedData({
            'version': CMSVersion(1),
            'certificates': certificates,
            'signer_infos': signer_infos,
            'digest_algorithms': das,
            'encap_content_info': encap_info,
        })

        sd.debug()

        return sd
        


class SCEPMessage(object):

    @classmethod
    def parse(cls, raw: bytes):
        msg = cls()

        cinfo = ContentInfo.load(raw)
        msg._signer_info = cinfo['content']['signer_infos'][0]
        msg._signed_data = cinfo['content']['encap_content_info']['content']

        # Signed Attrs always have the 'Any' type so should be parsed
        for cmsattr in cinfo['content']['signer_infos'][0]['signed_attrs']:
            name = asn1.SCEPCMSAttributeType.map(cmsattr['type'].native)

            if name == 'transaction_id':
                msg._transaction_id = cmsattr['values'][0].native
            elif name == 'message_type':
                msg._message_type = MessageType(cmsattr['values'][0].native)
            elif name == 'sender_nonce':
                msg._sender_nonce = cmsattr['values'][0].native
            elif name == 'recipient_nonce':
                msg._recipient_nonce = cmsattr['values'][0].native
            elif name == 'pki_status':
                msg._pki_status = cmsattr['values'][0].native

        return msg

    def __init__(self, message_type: MessageType = MessageType.CertRep, transaction_id=None, sender_nonce=None,
                 recipient_nonce=None):
        self._transaction_id = transaction_id
        self._message_type = message_type
        self._sender_nonce = sender_nonce
        self._recipient_nonce = recipient_nonce
        self._pki_status = None
        self._signer_info = None
        self._signed_data = None

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def message_type(self) -> MessageType:
        return self._message_type

    @property
    def sender_nonce(self) -> Union[bytes, None]:
        return self._sender_nonce

    @property
    def recipient_nonce(self) -> Union[bytes, None]:
        return self._recipient_nonce

    @property
    def pki_status(self):
        return self._pki_status

    @property
    def signer(self):
        sid = self._signer_info['sid']
        if isinstance(sid.chosen, IssuerAndSerialNumber):
            issuer = sid.chosen['issuer'].human_friendly
            serial = sid.chosen['serial_number'].native

            return issuer, serial

    @property
    def encap_content_info(self) -> ContentInfo:
        return ContentInfo.load(self._signed_data.native)

    @property
    def signed_data(self) -> SignedData:
        return self._signed_data

    @signed_data.setter
    def signed_data(self, value: SignedData):
        self._signed_data = value

    def get_decrypted_envelope_data(self, certificate: x509.Certificate, key: rsa.RSAPrivateKey) -> bytes:
        """Decrypt the encrypted envelope data:
        
        Decrypt encrypted_key using public key of CA
        encrypted_key is available at content.recipient_infos[x].encrypted_key
        algo is content.recipient_infos[x].key_encryption_algorithm
        at the moment this is RSA
        """
        encap = self.encap_content_info
        ct = encap['content_type'].native
        recipient_info = encap['content']['recipient_infos'][0]

        encryption_algo = recipient_info.chosen['key_encryption_algorithm'].native
        encrypted_key = recipient_info.chosen['encrypted_key'].native

        assert encryption_algo['algorithm'] == 'rsa'

        plain_key = key.decrypt(
            encrypted_key,
            padding=asympad.PKCS1v15(),
        )
        
        # Now we have the plain key, we can decrypt the encrypted data
        encrypted_contentinfo = encap['content']['encrypted_content_info']

        algorithm = encrypted_contentinfo['content_encryption_algorithm']  #: EncryptionAlgorithm
        encrypted_content_bytes = encrypted_contentinfo['encrypted_content'].native

        des_key = TripleDES(plain_key)
        cipher = Cipher(des_key, modes.CBC(algorithm.encryption_iv), backend=default_backend())
        decryptor = cipher.decryptor()

        return decryptor.update(encrypted_content_bytes) + decryptor.finalize()
