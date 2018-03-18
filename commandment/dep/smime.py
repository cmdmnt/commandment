import email
from email.message import Message
from base64 import b64decode
from asn1crypto.cms import EnvelopedData


def decrypt(file: str):
    with open(file, 'rb') as fd:
        string_content = fd.read().decode('utf8')
        msg: Message = email.message_from_string(string_content)
        assert msg.get_content_type() == 'application/pkcs7-mime'
        assert msg.get_filename() == 'smime.p7m'
        assert msg.get('Content-Description') == 'S/MIME Encrypted Message'

        b64payload = msg.get_payload()
        payload = b64decode(b64payload)
        enveloped_data = EnvelopedData.load(payload)

        