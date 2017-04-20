from enum import Enum

class EmailAccountType(Enum):
    POP = 'EmailTypePOP'
    IMAP = 'EmailTypeIMAP'


class EmailAuthenticationType(Enum):
    Password = 'EmailAuthPassword'
    CRAM_MD5 = 'EmailAuthCRAMMD5'
    NTLM = 'EmailAuthNTLM'
    HTTP_MD5 = 'EmailAuthHTTPMD5'
    ENone = 'EmailAuthNone'
