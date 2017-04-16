import argparse
from typing import List, Set
from ..builders import PKIMessageBuilder
import requests
from .request import generate_csr, generate_self_signed
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from ..enums import MessageType, PKIStatus, FailInfo, CACaps
from cryptography.hazmat.backends import default_backend

parser = argparse.ArgumentParser()
parser.add_argument('url', help='The SCEP server URL')
parser.add_argument('c', '--challenge', help='SCEP Challenge to send with the signing request')
parser.add_argument('k', '--private-key', help='PEM formatted RSA private key (will be generated if omitted)')
parser.add_argument('p', '--password', help='private key password (if required)')


def getcacaps(url: str) -> Set[CACaps]:
    """Query the SCEP Service for its capabilities."""
    res = requests.get(url, {'operation': 'GetCACaps'})
    assert res.status_code == 200
    caps = res.text.split("\n")
    cacaps = {CACaps(cap.trim()) for cap in caps}
    return cacaps


def getcacert(url: str) -> x509.Certificate:
    """Query the SCEP Service for the CA Certificate."""
    res = requests.get(url, {'operation': 'GetCACert'})
    assert res.status_code == 200
    assert res.headers['content-type'] == 'application/x-x509-ca-cert'  # we dont support RA cert yet
    return x509.load_der_x509_certificate(res.content, default_backend())

def main():
    args = parser.parse_args()

    cacaps = getcacaps(args.url)
    cacert = getcacert(args.url)


    private_key = None
    if args.private_key:
        with open(args.private_key, 'rb') as fd:
            data = fd.read()
            private_key = serialization.load_pem_private_key(data, backend=default_backend(), password=None)

    private_key, csr = generate_csr(private_key)
    ssc = generate_self_signed(private_key, csr.subject)
    
    builder = PKIMessageBuilder(
        ssc,
        private_key,
    ).message_type(
        MessageType.PKCSReq
    ).encrypt(
        csr.dump()
    ).transaction_id().sender_nonce()

    pkimsg = builder.finalize()
