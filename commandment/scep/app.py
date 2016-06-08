'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, request, Response, abort
from .message import *

scep_app = Blueprint('scep_app', __name__)

@scep_app.route('/cgi-bin/pkiclient.exe')
@scep_app.route('/')
def scep():
    op = request.args.get('operation')

    if op == 'GetCACert':
        # single sole CA
        cacert = open('commandment/scep/support/ca.crt', 'r').read()
        return Response(cacert, mimetype='application/x-x509-ca-cert')

    elif op == 'GetCACaps':
        return ''
    elif op == 'PKIOperation':
        msg = request.args.get('message')
        # Note: OS X improperly encodes the base64 query param by not encoding
        # spaces as %2B and instead leaving them as +'s. Correct for this.
        msg = msg.replace(' ', '+')
        msg = msg.decode('base64')

        pki_msg = PKIMessage.from_pkcs7_der(msg)

        print pki_msg.message_type

        return ''
    else:
        abort(404, 'invalid operation')
