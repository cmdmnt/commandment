import pytest
import os.path
from asn1crypto.cms import SignedAndEnvelopedData, ContentInfo, CMSAttribute
from asn1crypto.core import Sequence
from commandment.scep import asn1
from scep.message import SCEPMessage
from scep.ca import ca_from_storage


@pytest.fixture()
def pkcs7_der():
    with open(os.path.join('testdata', 'mdmclient-PKIOperation.bin'), 'rb') as fd:
        data = fd.read()
        return data


class TestSCEPOperations:

    # def test_parse_pkioperation(self, pkcs7_der: bytes):
    #     CMSAttribute._fields = [
    #         ('type', scep_message.SCEPCMSAttributeType),
    #         ('values', None),
    #     ]
    #
    #     sd = ContentInfo.load(pkcs7_der)
    #     sd['content']['signer_infos'].debug()

    def test_scep_message(self, pkcs7_der: bytes):
        m = SCEPMessage.from_pkcs7_der(pkcs7_der)
        print(m.transaction_id)
        print(m.message_type)
        print(m.sender_nonce)
        print(m.recipient_nonce)
        print(m.encap_content_info.debug())

        ca = ca_from_storage('/tmp/ca')
        d = m.get_decrypted_envelope_data(ca.certificate, ca.private_key)

