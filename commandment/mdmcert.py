'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, Response, render_template, request, make_response
from flask import redirect
# Response, request, current_app, abort, make_response
from .pki.ca import get_ca, PushCertificate
from .pki.x509 import CertificateRequest
from .models import (Certificate as DBCertificate,
                     PrivateKey as DBPrivateKey,
                     CertificateRequest as DBCertificateRequest)
from .database import db_session
import json
from base64 import b64encode
import urllib2
from M2Crypto import BIO, SMIME, X509, m2
import datetime
from .auth import require_auth

MDMCERT_REQ_URL = 'https://mdmcert.download/api/v1/signrequest'

# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

CERT_REQ_TYPE = 'mdmcert.pushcert'

def submit_mdmcert_request(email, pem_csr, pem_enc):
    mdmcert_dict = {
        'csr': b64encode(pem_csr),
        'email': email,
        'key': MDMCERT_API_KEY,
        'encrypt': b64encode(pem_enc),
    }

    req = urllib2.Request(
        MDMCERT_REQ_URL,
        json.dumps(mdmcert_dict),
        {'Content-Type': 'application/json',
         'User-Agent': 'coMmanDMent/0.1'})

    f = urllib2.urlopen(req)
    resp = f.read()
    f.close()

    return json.loads(resp)


class FixedLocationResponse(Response):
    # override Werkzeug default behaviour of "fixing up" once-non-compliant
    # relative location headers. now permitted in rfc7231 sect. 7.1.2
    autocorrect_location_header = False

admin_mdmcert_app = Blueprint('admin_mdmcert_app', __name__)

@admin_mdmcert_app.route('/')
def index():
    return render_template('admin/mdmcert/new.html')

@admin_mdmcert_app.route('/submit', methods=['POST'])
def submit():
    mdm_ca = get_ca()

    csr, csr_pk = CertificateRequest.with_new_private_key(CN='mdmcert.download')

    db_csr = DBCertificateRequest.from_x509(csr, CERT_REQ_TYPE)
    db_pk = DBPrivateKey.from_x509(csr_pk)

    db_pk.certificate_requests.append(db_csr)

    db_session.add(db_csr)
    db_session.add(db_pk)

    db_session.commit()

    email = request.form.get('email')

    res = submit_mdmcert_request(email, csr.to_pem(), mdm_ca.get_cacert().to_pem())
    print res.get('result')
    if res.get('result') != 'success':
        return 'Error! ' + res.get('reason', '')

    return 'Submitted!'

from binascii import unhexlify

@admin_mdmcert_app.route('/upload_encr', methods=['POST'])
def upload_encr():
    mdm_ca = get_ca()

    upl_encrypt = unhexlify(request.files['upload_encr_file'].stream.read())

    s = SMIME.SMIME()

    bio = BIO.MemoryBuffer(upl_encrypt)

    s.load_key_bio(
        BIO.MemoryBuffer(mdm_ca.get_private_key().to_pem()),
        BIO.MemoryBuffer(mdm_ca.get_cacert().to_pem()))

    p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(bio._ptr()))

    out = s.decrypt(p7)

    response = make_response(out)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=mdm_signed_request.%s.plist.b64' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return response

@admin_mdmcert_app.route('/upload_cert', methods=['POST'])
def upload_cert():
    pcert = PushCertificate.from_pem(request.files['upload_cert_file'].stream.read())

    cert_modulus = pcert._get_pubkey().get_modulus()

    q = db_session.query(DBCertificateRequest).filter(DBCertificateRequest.req_type == CERT_REQ_TYPE)
    for cr in q:
        req = cr.to_x509()
        if req._get_pubkey().get_modulus() == cert_modulus:
            db_cert = DBCertificate.from_x509(pcert, 'mdm.pushcert')

            db_pk = cr.privatekeys[0]

            db_pk.certificates.append(db_cert)

            db_session.add(db_cert)

            db_session.commit()

            return redirect('/admin/certificates', Response=FixedLocationResponse)


    return 'no matching CSR found'

@admin_mdmcert_app.before_request
def auth_check():
    return require_auth()
