'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, request, Response, abort, current_app
from .message import *
from M2Crypto import X509, EVP
from commandment.pki.m2certs import Certificate, CertificateRequest, RSAPrivateKey
from os import urandom
from ..pki.ca import get_ca
from ..database import db_session, NoResultFound
from ..models import SCEPConfig

FORCE_DEGENERATE_FOR_SINGLE_CERT = True
CACAPS = ('POSTPKIOperation', 'SHA-256', 'AES')

scep_app = Blueprint('scep_app', __name__)

def init_scep_record():
    try:
        db_session.query(SCEPConfig).one()
    except NoResultFound:
        scep_config = SCEPConfig(challenge=urandom(32).encode('hex'))
        db_session.add(scep_config)
        db_session.commit()

@scep_app.route('/cgi-bin/pkiclient.exe', methods=['GET', 'POST'])
@scep_app.route('/scep', methods=['GET', 'POST'])
@scep_app.route('/', methods=['GET', 'POST'])
def scep():
    op = request.args.get('operation')
    mdm_ca = get_ca()
    scep_config = db_session.query(SCEPConfig).one()

    if op == 'GetCACert':
        certs = [mdm_ca.get_cacert().get_m2_cert()]

        if len(certs) == 1 and not FORCE_DEGENERATE_FOR_SINGLE_CERT:
            return Response(certs[0].as_der(), mimetype='application/x-x509-ca-cert')
        elif len(certs):
            p7_degenerate = degenerate_pkcs7_der(certs)
            return Response(p7_degenerate, mimetype='application/x-x509-ca-ra-cert')
    elif op == 'GetCACaps':
        return '\n'.join(CACAPS)
    elif op == 'PKIOperation':
        if request.method == 'GET':
            msg = request.args.get('message')
            # note: OS X improperly encodes the base64 query param by not
            # encoding spaces as %2B and instead leaving them as +'s
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

            m2_evp_cakey = EVP.PKey()
            m2_evp_cakey.assign_rsa(mdm_ca.ca_privkey.get_m2_rsa(), capture=0)

            m2_x509_cacert = mdm_ca.get_cacert().get_m2_cert()

            req = pki_msg.get_decrypted_envelope_data(
                m2_x509_cacert,
                m2_evp_cakey)

            cert_req = CertificateRequest.load_der(req)

            # if get_challenge_password(cert_req) == scep_config.challenge:
            # else

            # sign request and save to DB
            new_cert, db_new_cert = mdm_ca.sign_new_device_req(cert_req)

            new_cert_degen = degenerate_pkcs7_der([new_cert.get_m2_cert()])

            repl_msg = CertRep()
            repl_msg.transaction_id = pki_msg.transaction_id
            repl_msg.signing_cert = m2_x509_cacert
            repl_msg.signing_pkey = m2_evp_cakey

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
        abort(404, 'unknown SCEP operation')
