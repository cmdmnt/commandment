from enum import IntFlag, auto, Enum


class Platform(Enum):
    macOS = 'macOS'
    iOS = 'iOS'
    tvOS = 'tvOS'


class AccessRights(IntFlag):
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
