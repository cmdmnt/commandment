from typing import Union
import os
from asn1crypto.core import Integer, PrintableString
from asn1crypto.cms import CMSAttribute, ContentInfo, EnvelopedData, EncapsulatedContentInfo
from commandment.scep import asn1
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.backends import default_backend

CMSAttribute._fields = [
    ('type', asn1.SCEPCMSAttributeType),
    ('values', None),
]


class SCEPMessage(object):

    def __init__(self, content: ContentInfo):
        self._content_info = content
        self._transaction_id = None
        self._message_type = None
        self._sender_nonce = None
        self._recipient_nonce = None

        # Signed Attrs always have the 'Any' type so should be parsed
        for cmsattr in self._content_info['content']['signer_infos'][0]['signed_attrs']:
            name = asn1.SCEPCMSAttributeType.map(cmsattr['type'].native)

            if name == 'transaction_id':
                self._transaction_id = cmsattr['values'][0].native
            elif name == 'message_type':
                self._message_type = asn1.SCEP_MESSAGE_TYPES[cmsattr['values'][0].native]
            elif name == 'sender_nonce':
                self._sender_nonce = cmsattr['values'][0].native
            elif name == 'recipient_nonce':
                self._recipient_nonce = cmsattr['values'][0].native
            elif name == 'pki_status':
                self._pki_status = cmsattr['values'][0].native
        
    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def message_type(self) -> str:
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
    def encap_content_info(self) -> ContentInfo:
        content = self._content_info['content']  # SignedData
        encapsulated_content_info = content['encap_content_info']['content']
        return ContentInfo.load(encapsulated_content_info.native)

    @classmethod
    def from_pkcs7_der(cls, msg: bytes):
        asn_data = ContentInfo.load(msg)
        return cls(asn_data)

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

