from enum import Enum
from uuid import uuid4, UUID
from typing import Dict, Set, List, Type, ClassVar, Any, Optional, Tuple
import semver
from base64 import urlsafe_b64encode, urlsafe_b64decode
from . import AccessRights, AccessRightsSet, Platform

PlatformVersion = str
PlatformRequirements = Dict[Platform, PlatformVersion]


class CommandRegistry(type):
    command_classes: Dict[str, Type] = {}

    def __new__(mcs, name, bases, namespace, **kwds):
        ns = dict(namespace)
        klass = type.__new__(mcs, name, bases, ns)
        if 'request_type' in ns:
            CommandRegistry.command_classes[ns['request_type']] = klass

        return klass


class Command(metaclass=CommandRegistry):

    # request_type: ClassVar[str] = None
    """request_type (str): The MDM RequestType, as specified in the MDM Specification."""

    # require_access: ClassVar[AccessRightsSet] = set()
    """require_access (Set[AccessRights]): Access required for the MDM to execute the command on this device."""

    # require_platforms: ClassVar[PlatformRequirements] = dict()
    """require_platforms (PlatformRequirements): A dict of Platform : version predicate string, to indicate which 
    platforms will accept the command"""

    # require_supervised: ClassVar[bool] = False
    """require_supervised (bool): This command requires supervision on iOS/tvOS"""

    def __init__(self, uuid=None) -> None:
        """The Command class wraps an MDM Request Command dict to provide validation and convenience methods for
        accessing command attributes.

        All commands are serialised to the same table as JSON, so the validation is performed here.

        Args:
            uuid (UUID): The command uuid. Defaults to an automatically generated uuid.
        """
        if uuid is None:
            uuid = uuid4()

        self._uuid: UUID = uuid
        self._attrs: Dict[str, Any] = {}
        # self.request_type: Optional[str] = None
        # self.require_access: AccessRightsSet = set()
        # self.require_platforms: PlatformRequirements = dict()
        # self.require_supervised: bool = False

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def parameters(self) -> Dict[str, Any]:
        return self._attrs

    @classmethod
    def new_request_type(cls, request_type: str, parameters: dict, uuid: str = None) -> 'Command':
        """Factory method for instantiating a command based on its class attribute ``request_type``.

        Additionally, the dict given in parameters will be applied to the command instance.
        Commands that have no parameters are not required to implement to_dict().

        Args:
              request_type (str): The command request type, as defined in the class attribute ``request_type``.
              parameters (dict): The parameters of this command instance.
              uuid (str): The command UUID. Optional, will be generated if omitted.
        Raises:
              ValueError if there is no command matching the request type given.
        Returns:
              Command class that corresponds to the request type given. Inherits from Command.
        """
        if request_type in CommandRegistry.command_classes:
            klass = CommandRegistry.command_classes[request_type]
            return klass(uuid, **parameters)
        else:
            raise ValueError('No such RequestType registered: {}'.format(request_type))

    def to_dict(self) -> dict:
        """Convert the command into a dict that will be serializable by plistlib.

        This default implementation will work for command types that have no parameters.
        """
        command = {'RequestType': self.request_type}

        return {
            'CommandUUID': str(self._uuid),
            'Command': command,
        }


class DeviceInformation(Command):
    request_type = 'DeviceInformation'
    require_access = {AccessRights.QueryDeviceInformation, AccessRights.QueryNetworkInformation}

    class Queries(Enum):
        """The Queries enumeration contains all possible Query types for the DeviceInformation command."""

        # Table 5 : General Queries
        UDID = 'UDID'
        Languages = 'Languages'
        Locales = 'Locales'
        DeviceID = 'DeviceID'
        OrganizationInfo = 'OrganizationInfo'
        LastCloudBackupDate = 'LastCloudBackupDate'
        AwaitingConfiguration = 'AwaitingConfiguration'
        AutoSetupAdminAccounts = 'AutoSetupAdminAccounts'

        # Table 6 : iTunes Account
        iTunesStoreAccountIsActive = 'iTunesStoreAccountIsActive'
        iTunesStoreAccountHash = 'iTunesStoreAccountHash'

        # Table 7 : Device Queries
        DeviceName = 'DeviceName'
        OSVersion = 'OSVersion'
        BuildVersion = 'BuildVersion'
        ModelName = 'ModelName'
        Model = 'Model'
        ProductName = 'ProductName'
        SerialNumber = 'SerialNumber'
        DeviceCapacity = 'DeviceCapacity'
        AvailableDeviceCapacity = 'AvailableDeviceCapacity'
        BatteryLevel = 'BatteryLevel'
        CellularTechnology = 'CellularTechnology'
        IMEI = 'IMEI'
        MEID = 'MEID'
        ModemFirmwareVersion = 'ModemFirmwareVersion'
        IsSupervised = 'IsSupervised'
        IsDeviceLocatorServiceEnabled = 'IsDeviceLocatorServiceEnabled'
        IsActivationLockEnabled = 'IsActivationLockEnabled'
        IsDoNotDisturbInEffect = 'IsDoNotDisturbInEffect'
        EASDeviceIdentifier = 'EASDeviceIdentifier'
        IsCloudBackupEnabled = 'IsCloudBackupEnabled'
        OSUpdateSettings = 'OSUpdateSettings'
        LocalHostName = 'LocalHostName'
        HostName = 'HostName'
        SystemIntegrityProtectionEnabled = 'SystemIntegrityProtectionEnabled'
        ActiveManagedUsers = 'ActiveManagedUsers'
        IsMDMLostModeEnabled = 'IsMDMLostModeEnabled'
        MaximumResidentUsers = 'MaximumResidentUsers'

        # Table 9 : Network Information Queries
        ICCID = 'ICCID'
        BluetoothMAC = 'BluetoothMAC'
        WiFiMAC = 'WiFiMAC'
        EthernetMACs = 'EthernetMACs'
        CurrentCarrierNetwork = 'CurrentCarrierNetwork'
        SIMCarrierNetwork = 'SIMCarrierNetwork'
        SubscriberCarrierNetwork = 'SubscriberCarrierNetwork'
        CarrierSettingsVersion = 'CarrierSettingsVersion'
        PhoneNumber = 'PhoneNumber'
        VoiceRoamingEnabled = 'VoiceRoamingEnabled'
        DataRoamingEnabled = 'DataRoamingEnabled'
        IsRoaming = 'IsRoaming'
        PersonalHotspotEnabled = 'PersonalHotspotEnabled'
        SubscriberMCC = 'SubscriberMCC'
        SubscriberMNC = 'SubscriberMNC'
        CurrentMCC = 'CurrentMCC'
        CurrentMNC = 'CurrentMNC'

        # Maybe undocumented
        CurrentConsoleManagedUser = 'CurrentConsoleManagedUser'

    Requirements = {
        'Languages': [
            (Platform.iOS, '>=7'),
            (Platform.tvOS, '>=6'),
            (Platform.macOS, '>=10.10'),
        ],
        'Locales': [
            (Platform.iOS, '>=7'),
            (Platform.tvOS, '>=6'),
            (Platform.macOS, '>=10.10'),
        ],
        'DeviceID': [
            (Platform.tvOS, '>=6'),
        ],
        'OrganizationInfo': [
            (Platform.iOS, '>=7'),
        ],
        'LastCloudBackupDate': [
            (Platform.iOS, '>=8'),
            (Platform.macOS, '>=10.10')
        ],
        'AwaitingConfiguration': [
            (Platform.iOS, '>=9'),
        ],
        'AutoSetupAdminAccounts': [
            (Platform.macOS, '>=10.11')
        ],
        'BatteryLevel': [
            (Platform.iOS, '>=5')
        ],
        'CellularTechnology': [
            (Platform.iOS, '>=4.2.6')
        ],
        'iTunesStoreAccountIsActive': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9')
        ],
        'iTunesStoreAccountHash': [
            (Platform.iOS, '>=8'),
            (Platform.macOS, '>=10.10')
        ],
        'IMEI': [
            (Platform.iOS, '*'),
        ],
        'MEID': [
            (Platform.iOS, '*'),
        ],
        'ModemFirmwareVersion': [
            (Platform.iOS, '*'),
        ],
        'IsSupervised': [
            (Platform.iOS, '>=6'),
        ],
        'IsDeviceLocatorServiceEnabled': [
            (Platform.iOS, '>=7'),
        ],
        'IsActivationLockEnabled': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9')
        ],
        'IsDoNotDisturbInEffect': [
            (Platform.iOS, '>=7'),
        ],
        'EASDeviceIdentifier': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9'),
        ],
        'IsCloudBackupEnabled': [
            (Platform.iOS, '>=7.1'),
        ],
        'OSUpdateSettings': [
            (Platform.macOS, '>=10.11'),
        ],
        'LocalHostName': [
            (Platform.macOS, '>=10.11'),
        ],
        'HostName': [
            (Platform.macOS, '>=10.11'),
        ],
        'SystemIntegrityProtectionEnabled': [
            (Platform.macOS, '>=10.12'),
        ],
        'ActiveManagedUsers': [
            (Platform.macOS, '>=10.11'),
        ],
        'IsMDMLostModeEnabled': [
            (Platform.iOS, '>=9.3'),
        ],
        'MaximumResidentUsers': [
            (Platform.iOS, '>=9.3'),
        ]
    }

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(DeviceInformation, self).__init__(uuid)
        self._attrs = kwargs

    @classmethod
    def for_platform(cls, platform: Platform, min_os_version: str, queries: Set[Queries] = None) -> 'DeviceInformation':
        """Generate a command that is compatible with the specified platform and OS version.

        Args:
              platform (Platform): Desired target platform
              min_os_version (str): Desired OS version
              queries (Set[Queries]): Desired Queries, or default to ALL queries.

        Returns:
              DeviceInformation instance with supported queries.
        """

        def supported(query) -> bool:
            if query not in cls.Requirements:
                return True

            platforms = cls.Requirements[query]
            for req_platform, req_min_version in platforms:
                if req_platform != platform:
                    continue

                # TODO: version checking
                return True  # semver only takes maj.min.patch
                #return semver.match(min_os_version, req_min_version)

            return False

        if queries is None:
            supported_queries = filter(supported, [q.value for q in cls.Queries])
        else:
            supported_queries = filter(supported, queries)

        return cls(Queries=list(supported_queries))

    @property
    def queries(self) -> Set[str]:
        return self._attrs.get('Queries')

    def to_dict(self) -> dict:
        """Convert the command into a dict that will be serializable by plistlib."""
        return {
            'CommandUUID': str(self._uuid),
            'Command': {
                'RequestType': type(self).request_type,
                'Queries': self._attrs.get('Queries', None),
            }
        }


class SecurityInfo(Command):
    request_type = 'SecurityInfo'
    require_access = {AccessRights.SecurityQueries}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(SecurityInfo, self).__init__(uuid)
        self._attrs = kwargs


class DeviceLock(Command):
    request_type = 'DeviceLock'
    require_access = {AccessRights.DeviceLockPasscodeRemoval}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(DeviceLock, self).__init__(uuid)
        self._attrs = kwargs

    def to_dict(self) -> dict:
        command = {
            'RequestType': type(self).request_type,
            'Message': self._attrs.get('Message', 'Device is locked'),
        }

        if 'PIN' in self._attrs:
            command['PIN'] = self._attrs['PIN']

        if 'PhoneNumber' in self._attrs:
            command['PhoneNumber'] = self._attrs['PhoneNumber']

        return {
            'CommandUUID': str(self._uuid),
            'Command': command,
        }


class ClearPasscode(Command):
    request_type = 'ClearPasscode'
    require_access = {AccessRights.DeviceLockPasscodeRemoval}
    require_platforms = {Platform.iOS: '*'}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(ClearPasscode, self).__init__(uuid)
        self._attrs = kwargs

    def to_dict(self) -> dict:
        return {
            'CommandUUID': str(self._uuid),
            'Command': {
                'RequestType': type(self).request_type,
                'UnlockToken': urlsafe_b64decode(self._attrs['UnlockToken'])
            }
        }


class ProfileList(Command):
    request_type = 'ProfileList'
    require_access = {AccessRights.ProfileInspection}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(ProfileList, self).__init__(uuid)
        self._attrs = kwargs


class InstallProfile(Command):
    request_type = 'InstallProfile'
    require_access = {AccessRights.ProfileInstallRemove}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(InstallProfile, self).__init__(uuid)
        self._attrs = kwargs

        if 'profile' in kwargs:
            profile_data = kwargs['profile'].data
            self._attrs['Payload'] = urlsafe_b64encode(profile_data).decode('utf-8')
            del self._attrs['profile']

    def to_dict(self) -> dict:
        return {
            'CommandUUID': str(self._uuid),
            'Command': {
                'RequestType': type(self).request_type,
                'Payload': urlsafe_b64decode(self._attrs['Payload']),
            }
        }


class RemoveProfile(Command):
    request_type = 'RemoveProfile'
    require_access = {AccessRights.ProfileInstallRemove}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(RemoveProfile, self).__init__(uuid)
        self._attrs = {
            'Identifier': kwargs.get('Identifier')
        }

    def to_dict(self) -> dict:
        """Convert the command into a dict that will be serializable by plistlib."""
        return {
            'CommandUUID': str(self._uuid),
            'Command': {
                'RequestType': type(self).request_type,
                'Identifier': self._attrs.get('Identifier', None),
            }
        }


class CertificateList(Command):
    request_type = 'CertificateList'
    require_access = {AccessRights.ProfileInspection}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(CertificateList, self).__init__(uuid)
        self._attrs = kwargs


class ProvisioningProfileList(Command):
    request_type = 'ProvisioningProfileList'
    require_access = {AccessRights.ProfileInspection}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs):
        super(ProvisioningProfileList, self).__init__(uuid)
        self._attrs = kwargs


class InstalledApplicationList(Command):
    request_type = 'InstalledApplicationList'
    require_access: Set[AccessRights] = set()

    def __init__(self, uuid: Optional[UUID]=None, **kwargs):
        super(InstalledApplicationList, self).__init__(uuid)
        self._attrs = {}
        self._attrs.update(kwargs)

    @property
    def managed_apps_only(self) -> Optional[bool]:
        return self._attrs.get('ManagedAppsOnly', None)

    @managed_apps_only.setter
    def managed_apps_only(self, value: bool) -> None:
        self._attrs['ManagedAppsOnly'] = value

    @property
    def identifiers(self) -> Optional[List[str]]:
        return self._attrs.get('Identifiers', None)

    @identifiers.setter
    def identifiers(self, bundle_ids: List[str]) -> None:
        """NOTE: setting identifiers for macOS 10.12 causes an exception in mdmclient."""
        self._attrs['Identifiers'] = bundle_ids

    def to_dict(self) -> dict:
        """Convert the command into a dict that will be serializable by plistlib."""
        command = self._attrs
        command.update({'RequestType': type(self).request_type})

        return {
            'CommandUUID': str(self._uuid),
            'Command': command,
        }


class InstallApplication(Command):
    request_type = 'InstallApplication'
    require_access = {AccessRights.ManageApps}

    def __init__(self, uuid: Optional[UUID]=None, **kwargs) -> None:
        super(InstallApplication, self).__init__(uuid)
        self._attrs = {}
        if 'application' in kwargs:
            app = kwargs['application']
            self._attrs['iTunesStoreID'] = app.itunes_store_id
            self._attrs['ManagementFlags'] = 1
            self._attrs['ChangeManagementState'] = 'Managed'
        else:
            self._attrs.update(kwargs)

    @property
    def itunes_store_id(self) -> Optional[int]:
        return self._attrs.get('iTunesStoreID', None)

    @itunes_store_id.setter
    def itunes_store_id(self, id: int):
        self._attrs['iTunesStoreID'] = id
        if 'Options' not in self._attrs:
            self._attrs['Options'] = {}
            if 'PurchaseMethod' not in self._attrs['Options']:
                self._attrs['Options']['PurchaseMethod'] = 1

    def to_dict(self) -> dict:
        cmd = super(InstallApplication, self).to_dict()
        cmd['Command'].update(self._attrs)
        print(cmd)
        return cmd


class ManagedApplicationList(Command):
    request_type = 'ManagedApplicationList'
    require_access = {AccessRights.ManageApps}


class RestartDevice(Command):
    request_type = 'RestartDevice'
    require_access = {AccessRights.DeviceLockPasscodeRemoval}
    require_platforms = {Platform.iOS: '>=10.3'}


class ShutDownDevice(Command):
    request_type = 'ShutDownDevice'
    require_access = {AccessRights.DeviceLockPasscodeRemoval}
    require_platforms = {Platform.iOS: '>=10.3', Platform.macOS: '>=10.13'}


class EraseDevice(Command):
    request_type = 'EraseDevice'
    require_access = {AccessRights.DeviceErase}
    require_platforms = {Platform.iOS: '*', Platform.macOS: '>=10.8'}


class RequestMirroring(Command):
    request_type = 'RequestMirroring'
    require_platforms = {Platform.iOS: '>=7', Platform.macOS: '>=10.10'}


class StopMirroring(Command):
    request_type = 'StopMirroring'
    require_platforms = {Platform.iOS: '>=7', Platform.macOS: '>=10.10'}
    require_supervised = True


class Restrictions(Command):
    request_type = 'Restrictions'
    require_access = {AccessRights.RestrictionQueries, AccessRights.ProfileInspection}


class UsersList(Command):
    request_type = 'UsersList'
    require_platforms = {Platform.iOS: '>=9.3'}


class LogOutUser(Command):
    request_type = 'LogOutUser'
    require_platforms = {Platform.iOS: '>=9.3'}


class DeleteUser(Command):
    request_type = 'DeleteUser'
    require_platforms = {Platform.iOS: '>=9.3'}


class EnableLostMode(Command):
    request_type = 'EnableLostMode'
    require_platforms = {Platform.iOS: '>=9.3'}
    require_supervised = True


class DisableLostMode(Command):
    request_type = 'DisableLostMode'
    require_platforms = {Platform.iOS: '>=9.3'}
    require_supervised = True


class DeviceLocation(Command):
    request_type = 'DeviceLocation'
    require_platforms = {Platform.iOS: '>=9.3'}
    require_supervised = True


class PlayLostModeSound(Command):
    request_type = 'PlayLostModeSound'
    require_platforms = {Platform.iOS: '>=10.3'}
    require_supervised = True


class AvailableOSUpdates(Command):
    request_type = 'AvailableOSUpdates'
    require_platforms = {Platform.macOS: '>=10.11', Platform.iOS: '>=4'}


class Settings(Command):
    request_type = 'Settings'
    require_platforms = {Platform.macOS: '>=10.9', Platform.iOS: '>=5.0'}
    require_access = {AccessRights.ChangeSettings}

    def __init__(self,
                 uuid: Optional[UUID]=None,
                 device_name: Optional[str]=None,
                 hostname: Optional[str]=None,
                 voice_roaming: Optional[bool]=None,
                 personal_hotspot: Optional[bool]=None,
                 wallpaper=None,
                 data_roaming: Optional[bool]=None,
                 bluetooth: Optional[bool]=None,
                 **kwargs) -> None:
        super(Settings, self).__init__(uuid)
        if 'settings' in kwargs:
            self._attrs['settings'] = kwargs['settings']
        else:
            self._attrs['settings']: List[Dict[str, Any]] = []

        if device_name is not None:
            self._attrs['settings'].append({
                'Item': 'DeviceName',
                'DeviceName': device_name,
            })

        if hostname is not None:
            self._attrs['settings'].append({
                'Item': 'HostName',
                'HostName': hostname,
            })

        if voice_roaming is not None:
            self._attrs['settings'].append({
                'Item': 'VoiceRoaming',
                'Enabled': voice_roaming,
            })

        if personal_hotspot is not None:
            self._attrs['settings'].append({
                'Item': 'PersonalHotspot',
                'Enabled': personal_hotspot,
            })

        if data_roaming is not None:
            self._attrs['settings'].append({
                'Item': 'DataRoaming',
                'Enabled': data_roaming,
            })

        if bluetooth is not None:
            self._attrs['settings'].append({
                'Item': 'Bluetooth',
                'Enabled': bluetooth,
            })

    def to_dict(self) -> dict:
        return {
            'CommandUUID': str(self._uuid),
            'Command': {
                'RequestType': type(self).request_type,
                'Settings': self._attrs['settings'],
            }
        }
