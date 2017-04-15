from typing import Union
from base64 import b64encode
from asn1crypto.cms import CMSAttribute, ContentInfo, SignedData, IssuerAndSerialNumber

from commandment.scep import asn1
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.backends import default_backend
from .enums import MessageType
from .builders import certificates_from_asn1

CMSAttribute._fields = [
    ('type', asn1.SCEPCMSAttributeType),
    ('values', None),
]


class SCEPMessage(object):

    @classmethod
    def parse(cls, raw: bytes):
        msg = cls()

        cinfo = ContentInfo.load(raw)
        assert cinfo['content_type'].native == 'signed_data'
        signed_data = cinfo['content']

        # convert certificates using cryptography lib since it is easier to deal with the decryption
        assert len(signed_data['certificates']) > 0
        certs = certificates_from_asn1(signed_data['certificates'])
        print('{} certificate(s) attached to signedData'.format(len(certs)))

        # Iterate through signers and verify the signature for each.
        # Set convenience attributes at the same time
        for signer_info in cinfo['content']['signer_infos']:
            # version can be 1 (issuerandserial) or 3 (subjectkeyidentifier)
            # assert signer_info['version'] == 1
            identifier = signer_info['sid'].chosen
            assert isinstance(identifier, IssuerAndSerialNumber)  # TODO: also support other signer ids

            signer_cert = None
            for c in certs:  # find signer cert
                if c.serial_number == identifier['serial_number'].native:  # TODO: also convert issuer
                    signer_cert = c
                    break

            assert signer_cert is not None

            sig_algo = signer_info['signature_algorithm'].signature_algo
            print('Using signature algorithm: {}'.format(sig_algo))
            hash_algo = signer_info['digest_algorithm']['algorithm'].native
            print('Using digest algorithm: {}'.format(hash_algo))

            if hash_algo == 'sha1':
                hasher = hashes.SHA1()
            elif hash_algo == 'sha256':
                hasher = hashes.SHA256()
            elif hash_algo == 'sha512':
                hasher = hashes.SHA512()
            else:
                raise ValueError('Unsupported hash algorithm: {}'.format(hash_algo))

            assert sig_algo == 'rsassa_pkcs1v15'  # We only support PKCS1v1.5
            verifier = signer_cert.public_key().verifier(
                signer_info['signature'].native,
                asympad.PKCS1v15(),
                hasher
            )

            verifier.update(signed_data['encap_content_info']['content'].native)
            if 'signed_attrs' in signer_info:
                print('signed attrs added to signature')
                verifier.update(signer_info['signed_attrs'].dump())

            verifier.verify()

            # Set the signer for convenience on the instance
            msg._signer_info = signer_info

            if 'signed_attrs' in signer_info:
                for signed_attr in signer_info['signed_attrs']:
                    name = asn1.SCEPCMSAttributeType.map(signed_attr['type'].native)

                    if name == 'transaction_id':
                        msg._transaction_id = signed_attr['values'][0].native
                    elif name == 'message_type':
                        msg._message_type = MessageType(signed_attr['values'][0].native)
                    elif name == 'sender_nonce':
                        msg._sender_nonce = signed_attr['values'][0].native
                    elif name == 'recipient_nonce':
                        msg._recipient_nonce = signed_attr['values'][0].native
                    elif name == 'pki_status':
                        msg._pki_status = signed_attr['values'][0].native
            
        msg._signed_data = cinfo['content']['encap_content_info']['content']

        return msg

    def __init__(self, message_type: MessageType = MessageType.CertRep, transaction_id=None, sender_nonce=None,
                 recipient_nonce=None):
        self._content_info = None
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

    def verify_signers(self):
        """Verify the signature provided by each SignerInfo"""
        

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
