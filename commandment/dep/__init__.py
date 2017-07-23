from typing import Set, Dict
from enum import Enum


class SetupAssistantStep(Enum):
    """This enumeration contains all possible steps of Setup Assistant that can be skipped."""
    Passcode = 'Passcode'
    Registration = 'Registration'
    Location = 'Location'
    Restore = 'Restore'
    AppleID = 'AppleID'
    TOS = 'TOS'
    Biometric = 'Biometric'
    Payment = 'Payment'
    Zoom = 'Zoom'
    DisplayTone = 'DisplayTone'
    Android = 'Android'
    Siri = 'Siri'
    Diagnostics = 'Diagnostics'
    HomeButtonSensitivity = 'HomeButtonSensitivity'
    FileVault = 'FileVault'

    # ATV
    TapToSetup = 'TapToSetup'
    ScreenSaver = 'ScreenSaver'

SkipSetupSteps = Set[SetupAssistantStep]


class DEPProfileRemovalStatus(Enum):
    SUCCESS = "SUCCESS"
    NOT_ACCESSIBLE = "NOT_ACCESSIBLE"
    FAILED = "FAILED"

SerialNumber = str
DEPProfileRemovals = Dict[SerialNumber, DEPProfileRemovalStatus]
