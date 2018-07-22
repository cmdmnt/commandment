"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from typing import Dict
from flask import Response
import json
from base64 import b64encode
import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization

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

    res = requests.post(
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
    pass