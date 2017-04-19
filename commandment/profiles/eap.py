from typing import Set
from enum import IntEnum


class EAPTypes(IntEnum):
    """EAP Types accepted by the EAPClient"""
    TLS = 13
    LEAP = 17
    EAP_SIM = 18
    TTLS = 21
    EAP_AKA = 23
    PEAP = 25
    EAP_FAST = 43

AcceptEAPTypes = Set[EAPTypes]

