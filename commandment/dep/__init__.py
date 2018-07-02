from typing import Set, Dict
from enum import Enum


class SetupAssistantStep(Enum):
    """This enumeration contains all possible steps of Setup Assistant that can be skipped.

    See Also:
          - `DEP Web Services: Define Profile <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW30>`_.
    """
    """Skips Apple ID setup."""
    AppleID = 'AppleID'
    """Skips Touch ID setup."""
    Biometric = 'Biometric'
    """Disables automatically sending diagnostic information."""
    Diagnostics = 'Diagnostics'
    """Skips DisplayTone setup."""
    DisplayTone = 'DisplayTone'
    """Disables Location Services."""
    Location = 'Location'
    """Hides and disables the passcode pane."""
    Passcode = 'Passcode'
    """Skips Apple Pay setup."""
    Payment = 'Payment'
    """Skips privacy pane."""
    Privacy = 'Privacy'
    """Disables restoring from backup."""
    Restore = 'Restore'
    """Disables Siri."""
    Siri = 'Siri'
    """Skips Terms and Conditions."""
    TOS = 'TOS'
    """Skips zoom setup."""
    Zoom = 'Zoom'
    """If the Restore pane is not skipped, removes Move from Android option from it."""
    Android = 'Android'
    """Skips the Home Button screen in iOS."""
    HomeButtonSensitivity = 'HomeButtonSensitivity'
    """Skips on-boarding informational screens for user education (“Cover Sheet, Multitasking & Control Center”, 
        for example) in iOS."""
    iMessageAndFaceTime = 'iMessageAndFaceTime'
    """Skips the iMessage and FaceTime screen in iOS."""
    OnBoarding = 'OnBoarding'
    """Skips the screen for watch migration in iOS."""
    WatchMigration = 'WatchMigration'
    """Disables FileVault Setup Assistant screen in macOS."""
    FileVault = 'FileVault'
    """Skips iCloud Analytics screen in macOS."""
    iCloudDiagnostics = 'iCloudDiagnostics'
    """Skips iCloud Documents and Desktop screen in macOS."""
    iCloudStorage = 'iCloudStorage'
    """Disables registration screen in macOS"""
    Registration = 'Registration'
      
    #  ATV
    """Skips the tvOS screen about using aerial screensavers in ATV."""
    ScreenSaver = 'ScreenSaver'
    """Skips the Tap To Set Up option in ATV about using an iOS device to set up your ATV (instead of entering all 
        your account information and setting choices separately)."""
    TapToSetup = 'TapToSetup'
    """Skips TV home screen layout sync screen in tvOS."""
    TVHomeScreenSync = 'TVHomeScreenSync'
    """Skips the TV provider sign in screen in tvOS."""
    TVProviderSignIn = 'TVProviderSignIn'
    """Skips the “Where is this Apple TV?” screen in tvOS."""
    TVRoom = 'TVRoom'


SkipSetupSteps = Set[SetupAssistantStep]


class DEPProfileRemovalStatus(Enum):
    SUCCESS = "SUCCESS"
    NOT_ACCESSIBLE = "NOT_ACCESSIBLE"
    FAILED = "FAILED"


SerialNumber = str
DEPProfileRemovals = Dict[SerialNumber, DEPProfileRemovalStatus]
