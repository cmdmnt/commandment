"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from typing import Dict
from flask import Response
import json
from base64 import b64encode
import requests
from binascii import unhexlify
from cryptography import x509
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization
from commandment.dep.smime import decrypt, decrypt_smime_content

MDMCERT_REQ_URL = 'https://mdmcert.download/api/v1/signrequest'

# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

CERT_REQ_TYPE = 'mdmcert.pushcert'


def submit_mdmcert_request(email: str, csr_pem: str,
                           encrypt_with_pem: str, api_key: str = MDMCERT_API_KEY) -> Dict:
    """Submit a CSR signing request to mdmcert.download.

    Note: Need to ``export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`` on High Sierra +

    Example Response:

        {'reason': 'Invalid email address. Have you registered yet at https://mdmcert.download/?', 'result': 'failure'}

        on success:

        {'result': 'success'}

    Args:
          email (str): Your registered mdmcert.download e-mail address.
          api_key (str): Your registered mdmcert.download API key.
          csr_pem (str): The MDM CSR to sign.
          encrypt_with_pem (str): The certificate which will be used to encrypt the response.

    Returns:
          dict: Response from the mdmcert.download service.
    """
    base64_csr = b64encode(csr_pem)
    base64_recipient = b64encode(encrypt_with_pem)

    mdmcert_dict = {
        'csr': base64_csr.decode('utf8'),
        'email': email,
        'key': api_key,
        'encrypt': base64_recipient.decode('utf8'),
    }

    session = requests.Session()

    # This was necessary because i had Charles proxy on macOS which caused the subprocess to abort trap 6. The reason
    # is interlinked with request's ability to read system proxy settings.
    session.trust_env = False  # Don't read proxy settings from OS.

    res = session.post(
        MDMCERT_REQ_URL,
        data=json.dumps(mdmcert_dict).encode('utf8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'coMmanDMent/0.1',
        })

    return res.json()


class FixedLocationResponse(Response):
    # override Werkzeug default behaviour of "fixing up" once-non-compliant
    # relative location headers. now permitted in rfc7231 sect. 7.1.2
    autocorrect_location_header = False


def decrypt_mdmcert(response: bytes, decrypt_with: RSAPrivateKeyWithSerialization) -> bytes:
    """Decrypt a .plist.b64.p7 supplied by mdmcert.download.

    In order to decrypt this we need to:
    - decode the payload using unhexlify()
    - find the private key that corresponded to the request.

    Args:
        response (bytes): The still encryped and hex encoded payload
        decrypt_with (RSAPrivateKeyWithSerialization): The private key that should be used to decrypt the payload.

    Returns:
        bytes - the decrypted response
    """
    decoded_payload = unhexlify(response)

    result = decrypt_smime_content(decoded_payload, decrypt_with)
    # result = decrypt_with.decrypt(
    #     decoded_payload,
    #     padding.PKCS7(block_size=8)
    # )
    return result
