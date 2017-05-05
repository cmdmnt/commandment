from typing import Set
from enum import Enum, IntEnum


class EAPTypes(IntEnum):
    """EAP Types accepted by the EAPClient.
    
    See Also:
          EAP8021X, EAP.h:51
    """
    Invalid = 0
    Identity = 1
    Notification = 2
    Nak = 3
    MD5Challenge = 4
    OneTimePassword = 5
    GenericTokenCard = 6
    TLS = 13
    CiscoLEAP = 17
    EAP_SIM = 18
    SRP_SHA1 = 19
    TTLS = 21
    EAP_AKA = 23
    PEAP = 25
    MSCHAPv2 = 26
    Extensions = 33
    EAP_FAST = 43
    EAP_AKA_Prime = 50

AcceptEAPTypes = Set[EAPTypes]


class TTLSInnerAuthentication(Enum):
    PAP = 'PAP'
    CHAP = 'CHAP'
    MSCHAP = 'MSCHAP'
    MSCHAPv2 = 'MSCHAPv2'
    EAP = 'EAP'
