from typing import Optional
import email
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES, AES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from email.message import Message
from base64 import b64decode
from asn1crypto.cms import EnvelopedData, ContentInfo, RecipientInfo, IssuerAndSerialNumber, KeyTransRecipientInfo, \
    RecipientIdentifier, EncryptionAlgorithm


def decrypt(smime: bytes, key: rsa.RSAPrivateKey, serial: Optional[int] = None):
    """Decrypt an S/MIME message using the RSA Private Key given.

    The recipient can be hinted using the serial parameter, otherwise we assume single recipient = the given key.
    """
    string_content = smime.decode('utf8')
    msg: Message = email.message_from_string(string_content)
    assert msg.get_content_type() == 'application/pkcs7-mime'
    assert msg.get_filename() == 'smime.p7m'
    assert msg.get('Content-Description') == 'S/MIME Encrypted Message'

    b64payload = msg.get_payload()
    payload = b64decode(b64payload)
    content_info = ContentInfo.load(payload)

    assert content_info['content_type'].native == 'enveloped_data'
    content: EnvelopedData = content_info['content']

    matching_recipient = content['recipient_infos'][0]

    # Need to see if we hold the key for any valid recipient.
    # for recipient_info in content['recipient_infos']:
    #     assert recipient_info.name == 'ktri'  # Only support KeyTransRecipientInfo
    #     ktri: KeyTransRecipientInfo = recipient_info.chosen
    #     recipient_id: RecipientIdentifier = ktri['rid']
    #     assert recipient_id.name == 'issuer_and_serial_number'  # Only support IssuerAndSerialNumber
    #     matching_recipient = recipient_info

    encryption_algo = matching_recipient.chosen['key_encryption_algorithm'].native
    encrypted_key = matching_recipient.chosen['encrypted_key'].native

    assert encryption_algo['algorithm'] == 'rsa'

    # Get the content key
    plain_key = key.decrypt(
        encrypted_key,
        padding=padding.PKCS1v15(),
    )

    # Now we have the plain key, we can decrypt the encrypted data
    encrypted_contentinfo = content['content']['encrypted_content_info']
    print('encrypted content type: {}'.format(encrypted_contentinfo['content_type'].native))

    algorithm: EncryptionAlgorithm = encrypted_contentinfo['content_encryption_algorithm']  #: EncryptionAlgorithm
    encrypted_content_bytes = encrypted_contentinfo['encrypted_content'].native

    symkey = None

    if algorithm.encryption_cipher == 'aes':
        symkey = AES(plain_key)
        print('cipher AES')
    elif algorithm.encryption_cipher == 'tripledes':
        symkey = TripleDES(plain_key)
        print('cipher 3DES')
    else:
        print('Dont understand encryption cipher: ', algorithm.encryption_cipher)

    print('key length: ', algorithm.key_length)
    print('enc mode: ', algorithm.encryption_mode)

    cipher = Cipher(symkey, modes.CBC(algorithm.encryption_iv), backend=default_backend())
    decryptor = cipher.decryptor()

    return decryptor.update(encrypted_content_bytes) + decryptor.finalize()
