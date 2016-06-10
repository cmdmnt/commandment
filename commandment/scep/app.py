'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, request, Response, abort, current_app
from .message import *
from M2Crypto import X509, EVP
from commandment.pki.m2certs import Certificate, CertificateRequest, RSAPrivateKey
from os import urandom

FORCE_DEGENERATE_FOR_SINGLE_CERT = True

scep_app = Blueprint('scep_app', __name__)

@scep_app.route('/cgi-bin/pkiclient.exe', methods=['GET', 'POST'])
@scep_app.route('/scep', methods=['GET', 'POST'])
@scep_app.route('/', methods=['GET', 'POST'])
def scep():
    op = request.args.get('operation')

    if op == 'GetCACert':
        certs = [X509.load_cert('commandment/scep/support/ca.crt')]

        if len(certs) == 1 and not FORCE_DEGENERATE_FOR_SINGLE_CERT:
            return Response(certs[0].as_der(), mimetype='application/x-x509-ca-cert')
        elif len(certs):
            x = degenerate_pkcs7_der(certs)
            open('/tmp/degen.p7', 'w').write(x)
            return Response(x, mimetype='application/x-x509-ca-ra-cert')
    elif op == 'GetCACaps':
        # TODO: SHA-2 and AES req'd?
        return 'POSTPKIOperation'
    elif op == 'PKIOperation':
        if request.method == 'GET':
            msg = request.args.get('message')
            # Note: OS X improperly encodes the base64 query param by not encoding
            # spaces as %2B and instead leaving them as +'s. Correct for this.
            msg = msg.replace(' ', '+')
            msg = msg.decode('base64')
        elif request.method == 'POST':
            # workaround for Flask/Werkzeug lack of chunked handling
            if 'chunked' in request.headers.get('Transfer-Encoding', ''):
                msg = request.environ['body_copy']
            else:
                msg = request.data

        pki_msg = SCEPMessage.from_pkcs7_der(msg)

        if pki_msg.message_type == PKCSReq.message_type:
            current_app.logger.debug('received PKCSReq SCEP message')

            req = pki_msg.get_decrypted_envelope_data(
                X509.load_cert('commandment/scep/support/ca.crt'),
                EVP.load_key('commandment/scep/support/ca.key'))

            cert_req = CertificateRequest.load_der(req)

            ca_cert = Certificate.load_file('commandment/scep/support/ca.crt')
            ca_key = RSAPrivateKey.load_file('commandment/scep/support/ca.key')

            new_cert = Certificate.cert_from_req_signed_by_cacert(
                cert_req, ca_cert, ca_key, serial=22)

            new_cert_degen = degenerate_pkcs7_der([new_cert.get_m2_cert()])

            repl_msg = CertRep()
            repl_msg.transaction_id = pki_msg.transaction_id
            repl_msg.signing_cert = X509.load_cert('commandment/scep/support/ca.crt')
            repl_msg.signing_pkey = EVP.load_key('commandment/scep/support/ca.key')

            repl_msg.signedcontent = new_cert_degen
            repl_msg.encrypt_envelope_data(pki_msg.signing_cert)

            repl_msg.recipient_nonce = pki_msg.sender_nonce
            repl_msg.sender_nonce = urandom(16)
            repl_msg.pki_status = PKI_STATUS_SUCCESS

            return Response(repl_msg.to_pkcs7_der(), mimetype='application/x-pki-message')
        else:
            current_app.logger.error('unhandled SCEP message type: %d', pki_msg.message_type)
            return ''
    else:
        abort(404, 'invalid operation')
