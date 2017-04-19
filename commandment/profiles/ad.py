from typing import Set
from enum import Enum, Flag, auto


class ADMountStyle(Enum):
    AFP = 'afp'
    SMB = 'smb'


class ADNamespace(Enum):
    Domain = 'domain'
    Forest = 'forest'


class ADOption(Flag):
    CreateMobileAccountAtLogin = auto()
    WarnUserBeforeCreatingMobileAccount = auto()
    ForceHomeLocal = auto()
    UseWindowsUNCPath = auto()
    AllowMultiDomainAuth = auto()

ADOptions = Set[ADOption]


class ADPacketSignPolicy(Enum):
    Allow = 'allow'
    Disable = 'disable'
    Require = 'require'


class ADPacketEncryptPolicy(Enum):
    Allow = 'allow'
    Disable = 'disable'
    Require = 'require'
    SSL = 'ssl'
