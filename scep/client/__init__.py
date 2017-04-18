import argparse
import logging

from typing import List, Set
from ..builders import PKIMessageBuilder, Signer
from ..envelope import PKCSPKIEnvelopeBuilder
import requests
from .request import generate_csr, generate_self_signed
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from ..enums import MessageType, PKIStatus, FailInfo, CACaps
from cryptography.hazmat.backends import default_backend
from ..message import SCEPMessage
from asn1crypto.cms import ContentInfo

parser = argparse.ArgumentParser()
parser.add_argument('url', help='The SCEP server URL')
parser.add_argument('-c', '--challenge', help='SCEP Challenge to send with the signing request')
parser.add_argument('-k', '--private-key', help='PEM formatted RSA private key (will be generated if omitted)')
parser.add_argument('-p', '--password', help='private key password (if required)')
parser.add_argument('-d', '--debug', help='enable debug mode', action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.WARNING)
parser.add_argument('--dump-pkcsreq', help='dump PKCSReq.bin to path given')

logger = logging.getLogger(__name__)


def getcacaps(url: str) -> Set[CACaps]:
    """Query the SCEP Service for its capabilities."""
    res = requests.get(url, {'operation': 'GetCACaps'})
    if res.status_code != 200:
        raise ValueError('Got invalid status code for GetCACaps: {}'.format(res.status_code))
    caps = res.text.split("\n")
    cacaps = {CACaps(cap.strip()) for cap in caps}
    return cacaps


def getcacert(url: str) -> x509.Certificate:
    """Query the SCEP Service for the CA Certificate."""
    res = requests.get(url, {'operation': 'GetCACert'})
    assert res.status_code == 200
    assert res.headers['content-type'] == 'application/x-x509-ca-cert'  # we dont support RA cert yet
    return x509.load_der_x509_certificate(res.content, default_backend())


def pkioperation(url: str, data: bytes):
    """Perform a PKIOperation using the CMS data given."""
    res = requests.post('{}?operation=PKIOperation'.format(url), data=data,
                        headers={'content-type': 'application/x-pki-message'})
    return res


def main():
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    logger.info('Request: GetCACaps')
    cacaps = getcacaps(args.url)
    logger.info(cacaps)
    logger.info('Request: GetCACert')
    cacert = getcacert(args.url)
    logger.info('CA Certificate Subject Follows')
    logger.info(cacert.subject)

    private_key = None
    if args.private_key:
        with open(args.private_key, 'rb') as fd:
            data = fd.read()
            private_key = serialization.load_pem_private_key(data, backend=default_backend(), password=None)

    private_key, csr = generate_csr(private_key)
    logger.info('Writing RSA private key to ./scep.key')
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open('scep.key', 'wb') as fd:
        fd.write(pem)
    
    ssc = generate_self_signed(private_key, csr.subject)

    envelope, key, iv = PKCSPKIEnvelopeBuilder().encrypt(
        csr.public_bytes(serialization.Encoding.DER)
    ).add_recipient(cacert).finalize()

    signer = Signer(ssc, private_key)

    pki_msg_builder = PKIMessageBuilder().message_type(
        MessageType.PKCSReq
    ).pki_envelope(
        envelope
    ).add_signer(
        signer
    ).transaction_id().sender_nonce()

    pki_msg = pki_msg_builder.finalize()
    
    if args.dump_pkcsreq:
        with open(args.dump_pkcsreq, 'wb') as fd:
            fd.write(pki_msg.dump())
        logger.info('Dumped PKCSReq data to {}'.format(args.dump_pkcsreq))

    res = pkioperation(args.url, data=pki_msg.dump())

    logger.info('Response: Status {}'.format(res.status_code))
    if res.status_code != 200:
        return -1

    cinfo = ContentInfo.load(res.content)
    cinfo.debug()
    cert_rep = SCEPMessage.parse(res.content)
    with open('certrep.der', 'wb') as fd:
        fd.write(res.content)
    logger.info('Dumped CertRep')

    logger.debug('pkiMessage response follows')
    logger.debug('Transaction ID: %s', cert_rep.transaction_id)
    logger.debug('PKI Status: %s', PKIStatus(cert_rep.pki_status))

    # This should be the PKCS#7 Degenerate
    decrypted_bytes = cert_rep.get_decrypted_envelope_data(ssc, private_key)
    degenerate_info = ContentInfo.load(decrypted_bytes)
    # degenerate_info.debug()

    assert degenerate_info['content_type'].native == 'signed_data'
    signed_response = degenerate_info['content']
    certs = signed_response['certificates']

    certs.debug()

    my_cert = certs[0].chosen
    result = x509.load_der_x509_certificate(my_cert.dump(), default_backend())
    print(result.subject)



