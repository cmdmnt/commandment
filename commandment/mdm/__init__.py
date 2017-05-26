from enum import IntFlag, auto, Enum


class Platform(Enum):
    """The platform of the managed device."""
    Unknown = 'Unknown'  # Not enough information
    macOS = 'macOS'
    iOS = 'iOS'
    tvOS = 'tvOS'


class AccessRights(IntFlag):
    """The MDM protocol defines a bitmask for granting permissions to an MDM to perform certain operations.
    
    This enumeration contains all of those access rights flags.
    """
    def _generate_next_value_(name, start, count, last_values):
        return 2 ** count

    ProfileInspection = auto()
    ProfileInstallRemove = auto()
    DeviceLockPasscodeRemoval = auto()
    DeviceErase = auto()
    QueryDeviceInformation = auto()
    QueryNetworkInformation = auto()
    ProvProfileInspection = auto()
    ProvProfileInstallRemove = auto()
    InstalledApplications = auto()
    RestrictionQueries = auto()
    SecurityQueries = auto()
    ChangeSettings = auto()
    ManageApps = auto()

    All = ProfileInspection | ProfileInstallRemove | DeviceLockPasscodeRemoval | DeviceErase | QueryDeviceInformation \
          | QueryNetworkInformation | ProvProfileInspection | ProvProfileInstallRemove | InstalledApplications \
          | RestrictionQueries | SecurityQueries | ChangeSettings | ManageApps


class CommandStatus(Enum):
    """CommandStatus describes all the possible states of a command in the device command queue."""
    #: str: Command has been created but has not been sent.
    Queued = 'Q'
    #: str: Command has been sent to the device, but no response has returned.
    Sent = 'S'
    #: str: Response has been returned from the device. This is considered completed
    Acknowledged = 'A'
    #: str: The command that we sent was invalid, unable to be processed.
    Invalid = 'I'
    #: str: The device is busy, this command cannot be processed right now.
    NotNow = 'N'
    #  str: This command is considered dead because it timed out, the device timed out, or was orphaned by a
    #  removed device.
    Expired = 'E'
