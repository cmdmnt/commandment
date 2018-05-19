"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from typing import Dict
from flask import Blueprint, Response
import json
from base64 import b64encode
import urllib.request, urllib.error, urllib.parse
from cryptography import x509
from cryptography.hazmat.primitives import serialization

MDMCERT_REQ_URL = 'https://mdmcert.download/api/v1/signrequest'

# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

CERT_REQ_TYPE = 'mdmcert.pushcert'


def submit_mdmcert_request(email: str, csr: x509.CertificateSigningRequest,
                           encrypt_with: x509.Certificate, api_key: str = MDMCERT_API_KEY) -> Dict:
    """Submit a CSR signing request to mdmcert.download.

    Args:
          email (str): Your registered mdmcert.download e-mail address.
          api_key (str): Your registered mdmcert.download API key.
          csr (cryptography.x509.CertificateSigningRequest): The MDM CSR to sign.
          encrypt_with (cryptography.x509.Certificate): The certificate which will be used to encrypt the response.

    Returns:
          dict: Response from the mdmcert.download service.
    """
    base64_csr = b64encode(csr.public_bytes(serialization.Encoding.PEM))
    base64_recipient = b64encode(encrypt_with.public_bytes(serialization.Encoding.PEM))

    mdmcert_dict = {
        'csr': base64_csr.decode('utf8'),
        'email': email,
        'key': api_key,
        'encrypt': base64_recipient.decode('utf8'),
    }

    req = urllib.request.Request(
        MDMCERT_REQ_URL,
        json.dumps(mdmcert_dict).encode('utf8'),
        {'Content-Type': 'application/json',
         'User-Agent': 'coMmanDMent/0.1'})

    f = urllib.request.urlopen(req)
    resp = f.read()
    f.close()

    return json.loads(resp)


class FixedLocationResponse(Response):
    # override Werkzeug default behaviour of "fixing up" once-non-compliant
    # relative location headers. now permitted in rfc7231 sect. 7.1.2
    autocorrect_location_header = False

admin_mdmcert_app = Blueprint('admin_mdmcert_app', __name__)


#
# from binascii import unhexlify
#
# @admin_mdmcert_app.route('/upload_encr', methods=['POST'])
# def upload_encr():
#     mdm_ca = get_ca()
#
#     upl_encrypt = unhexlify(request.files['upload_encr_file'].stream.read())
#
#     s = SMIME.SMIME()
#
#     bio = BIO.MemoryBuffer(upl_encrypt)
#
#     s.load_key_bio(
#         BIO.MemoryBuffer(mdm_ca.get_private_key().to_pem()),
#         BIO.MemoryBuffer(mdm_ca.get_cacert().to_pem()))
#
#     p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(bio._ptr()))
#
#     out = s.decrypt(p7)
#
#     response = make_response(out)
#     response.headers['Content-Type'] = 'application/octet-stream'
#     response.headers['Content-Disposition'] = 'attachment; filename=mdm_signed_request.%s.plist.b64' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#     return response
#

