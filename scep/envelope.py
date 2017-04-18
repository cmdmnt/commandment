import os
from asn1crypto.cms import RecipientInfo, KeyTransRecipientInfo, RecipientIdentifier, KeyEncryptionAlgorithm, \
    KeyEncryptionAlgorithmId, EnvelopedData, EncryptedContentInfo, ContentType, IssuerAndSerialNumber, RecipientInfos
from asn1crypto.core import OctetString

from cryptography.hazmat.primitives.asymmetric import padding as asympad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import serialization, hashes
from oscrypto.keys import parse_certificate
from typing import Tuple
from asn1crypto.algos import EncryptionAlgorithmId, EncryptionAlgorithm
from cryptography import x509


class PKCSPKIEnvelopeBuilder(object):
    """Build a PKCSPKIEnvelope (envelopedData + encryptedContentInfo) as per SCEP RFC
    
    This builder encrypts content and adds recipients who may decrypt that content.
    """

    def __init__(self):
        self._data = None
        self._encryption_algorithm_id = None
        self._recipients = []

    def encrypt(self, data: bytes, algorithm: str = None):
        """Set the data to be encrypted.
        
        The algorithm option is not yet available, and will default to 3DES-CBC.
        
        Args:
              data (bytes): The data to encrypt
              algorithm (str): RESERVED FOR FUTURE USE
        Returns:
              PKCSPKIEnvelopeBuilder
        """
        self._data = data
        self._encryption_algorithm_id = EncryptionAlgorithmId('tripledes_3key')

        return self

    def add_recipient(self, certificate: x509.Certificate):
        """Add a recipient for the encrypted data.
        
        Args:
              certificate (x509.Certificate): The recipients certificate, used to encrypt the symmetric key.
        Returns:
              PKCSPKIEnvelopeBuilder
        """
        self._recipients.append(certificate)

        return self

    def _encrypt_data(self, data: bytes) -> Tuple[TripleDES, bytes, bytes]:
        """Build the ciphertext of the ``messageData``.

        Args:
              data (bytes): Data to encrypt as the ``messageData`` of the SCEP Request

        Returns:
              Tuple of 3DES key, IV, and cipher text encrypted with 3DES
        """
        des_key = TripleDES(os.urandom(24))
        iv = os.urandom(8)
        cipher = Cipher(des_key, modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = PKCS7(TripleDES.block_size).padder()
        padded = padder.update(data)
        padded += padder.finalize()

        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return des_key, iv, ciphertext

    def _build_recipient_info(self, symmetric_key: bytes, recipient: x509.Certificate) -> RecipientInfo:
        """Build an ASN.1 data structure containing the encrypted symmetric key for the encrypted_content.
        
        NOTE: The recipient is always identified by issuerAndSerialNumber
        NOTE: 

        Args:
            symmetric_key (bytes): Typically the randomly generated 3DES key for the encrypted_content.
            recipient (x509.Certificate): The certificate which will be used to encrypt the symmetric key.

        Returns:
              RecipientInfo: Instance of ASN.1 data structure with required attributes and encrypted key.
        """
        encrypted_symkey = recipient.public_key().encrypt(
            symmetric_key,
            asympad.PKCS1v15()
        )
        asn1cert = parse_certificate(recipient.public_bytes(serialization.Encoding.DER))
        ias = IssuerAndSerialNumber({
            'issuer': asn1cert.issuer,
            'serial_number': asn1cert.serial_number
        })

        ri = RecipientInfo('ktri', KeyTransRecipientInfo({
            'version': 0,
            'rid': RecipientIdentifier('issuer_and_serial_number', ias),
            'key_encryption_algorithm': KeyEncryptionAlgorithm({'algorithm': KeyEncryptionAlgorithmId('rsa')}),
            'encrypted_key': encrypted_symkey,
        }))

        return ri

    def finalize(self) -> Tuple[EnvelopedData, TripleDES, bytes]:
        """Encrypt the data and process the key using all available recipients.
        
        Returns:
              EnvelopedData, TripleDES, iv (bytes): The PKCSPKIEnvelope structure, The symmetric key, and the IV for
              the symmetric key.
        """
        des_key, iv, ciphertext = self._encrypt_data(self._data)

        eci = EncryptedContentInfo({
            'content_type': ContentType('data'),
            'content_encryption_algorithm': EncryptionAlgorithm({
                'algorithm': EncryptionAlgorithmId('tripledes_3key'),
                'parameters': OctetString(iv),
            }),
            'encrypted_content': ciphertext,
        })

        recipients = [self._build_recipient_info(des_key.key, recipient) for recipient in self._recipients]
        recipient_infos = RecipientInfos(recipients)

        ed = EnvelopedData({
            'version': 1,
            'recipient_infos': recipient_infos,
            'encrypted_content_info': eci,
        })

        return ed, des_key, iv
