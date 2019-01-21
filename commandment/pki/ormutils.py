from typing import Optional

from asn1crypto.cms import ContentInfo, EnvelopedData, KeyTransRecipientInfo, RecipientIdentifier

from commandment.pki.models import Certificate


def find_recipient(cms_data: bytes) -> Optional[Certificate]:
    """Find the Certificate + Private Key of a recipient indicated by encoded CMS/PKCS#7 data from the database and
    return the database model that matches (if any).

    Requires that the indicated recipient is present in the `certificates` table, and has a matching private key in the
    `rsa_private_keys` table.
    """
    content_info = ContentInfo.load(cms_data)

    assert content_info['content_type'].native == 'enveloped_data'
    content: EnvelopedData = content_info['content']

    for recipient_info in content['recipient_infos']:
        if recipient_info.name == 'ktri':  # KeyTransRecipientInfo
            recipient: KeyTransRecipientInfo = recipient_info.chosen
            recipient_id: RecipientIdentifier = recipient['rid']
            assert recipient_id.name == 'issuer_and_serial_number'

        else:
            pass  # Unsupported recipient type

    return None

