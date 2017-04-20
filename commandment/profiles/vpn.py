from enum import Enum

class VPNType(Enum):
    L2TP = 'L2TP'
    PPTP = 'PPTP'
    IPSec = 'IPSec'
    IKEv2 = 'IKEv2'
    AlwaysOn = 'AlwaysOn'
    VPN = 'VPN'
