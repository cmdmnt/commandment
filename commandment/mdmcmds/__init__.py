'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from uuid import uuid4
from ..database import db_session
from ..models import QueuedCommand, Profile as DBProfile, MDMConfig
from ..profiles import Profile
from ..mdm import enroll
from flask import current_app
import json
import plistlib # needed for Data() wrapper

# Status = Acknowledged, Error, CommandFormatError, Idle, NotNow

class QueuedMDMCommand(object):
    def __init__(self, uuid=None, input_data={}, device=None):
        self.uuid = uuid if uuid else str(uuid4()).upper()
        self.input_data = input_data
        self.device = device

    def to_new_queued_command(self):
        qc = QueuedCommand()
        qc.uuid = self.uuid
        qc.command_class = self.__class__.__name__
        qc.input_data = self.input_data if self.input_data else None
        qc.device = self.device
        return qc

    @classmethod
    def new_queued_command(cls, device, input_data={}):
        new_qmc = cls(input_data=input_data, device=device)
        queued_cmd = new_qmc.to_new_queued_command()
        return queued_cmd

    @classmethod
    def from_queued_command(cls, device, queued_command):
        '''Load new command from class method'''
        return cls(uuid=queued_command.uuid, input_data=queued_command.input_data, device=device)

    def generate_command_dict(self):
        raise NotImplementedError

    def generate_dict(self):
        if not hasattr(self, 'request_type'):
            raise NotImplementedError('QueuedMDMCommand-derived class must have "request_type" attribute')

        cmd_dict = {
            'CommandUUID': self.uuid,
            'Command': {
                'RequestType': self.request_type,
            }
        }

        cmd_dict['Command'].update(self.generate_command_dict())

        return cmd_dict

    def process_response_dict(self, response):
        raise NotImplementedError


def find_mdm_command_class(command_name):
    '''Iterate through inherited classes to find a matching class name'''
    subclasses = set()
    work = [QueuedMDMCommand]
    while work:
        parent_subclass = work.pop()
        for child_subclass in parent_subclass.__subclasses__():
            if child_subclass not in subclasses:
                if child_subclass.__name__ == command_name:
                    return child_subclass

                subclasses.add(child_subclass)
                work.append(child_subclass)

    return None

QUERIES_ALL = [
    'UDID',
    'Languages', # iOS >= 7; ATV >= 6
    'Locales', # iOS >= 7; ATV >= 6
    'DeviceID', # iOS >= 7; ATV >= 6
    'LastCloudBackupDate', # iOS >= 8; OS X >= 10.10
    ]

QUERIES_INSTALL_APP = [
    'iTunesStoreAccountIsActive', # iOS >= 7; OS X >= 10.9
    'iTunesStoreAccountHash', # iOS >= 8; OS X >= 10.10
]

QUERIES_DEVICE_INFO = [
    'DeviceName',
    'OSVersion',
    'BuildVersion',
    'ModelName',
    'Model',
    'ProductName',
    'SerialNumber',
    'DeviceCapacity',
    'AvailableDeviceCapacity',
    'BatteryLevel', # iOS >= 5
    'CellularTechnology', # iOS >= 4.2.6
    'IMEI',
    'MEID',
    'ModemFirmwareVersion',
    'IsSupervised',
    'IsDeviceLocatorServiceEnabled',
    'IsActivationLockEnabled',
    'IsDoNotDisturbInEffect',
    'DeviceID',
    'EASDeviceIdentifier',
    'IsCloudBackupEnabled',
]

QUERIES_NETWORK_INFO = [
    # TODO
]

QUERIES_SECURITY_INFO = [
    # TODO
]

class UpdateInventoryDevInfoCommand(QueuedMDMCommand):
    '''Query device information and store result on the device object'''
    request_type = 'DeviceInformation'
    def generate_command_dict(self):
        return {'Queries': QUERIES_ALL + QUERIES_INSTALL_APP + QUERIES_DEVICE_INFO}

    def process_response_dict(self, result):
        self.device.info_json = result['QueryResponses']
        existing_serial_number = self.device.serial_number
        self.device.serial_number = result['QueryResponses'].get('SerialNumber')
        current_app.logger.info("Got device info (%s)" % str(existing_serial_number))
        if not existing_serial_number:
            current_app.logger.info("... for the first time")
            enroll.notify_serial_first_received(self.device.udid, self.device.serial_number)
        if 'Locales' in result:
            # Locales key seems quite verbose on OS X, just strip it for now
            del result['Locales']
        db_session.commit()

        # TODO: search for existing serial number and possibly merge records?

'''
List of MDM Request Types (commands):

ProfileList
InstallProfile
RemovePofile
ProvisioningProfileList
RemoveProvisioningProfile
CertificateList
InstalledApplicationList
DeviceInformation
SecurityInfo
DeviceLock
ClearPasscode
EraseDevice
RequestMirroring
StopMirroring
Restrictions
ClearRestrictionsPassword
InstallApplication
ApplyRedemptionCode
ManagedApplicationList
RemoveApplication
InviteToProgram
InstallMedia
ManagedMediaList
RemoveMedia
Settings
ManagedApplicationConfiguration
ManagedApplicationAttributes
ManagedApplicationFeedback
'''

import pprint

class GenericQueryProfiles(QueuedMDMCommand):
    request_type = 'ProfileList'
    def generate_command_dict(self):
        return {}

    def process_response_dict(self, result):
        print 'QueryProfiles.process_response_dict() called'
        pprint.pprint(result)

class RemoveProfile(QueuedMDMCommand):
    request_type = 'RemoveProfile'
    def generate_command_dict(self):
        return {'Identifier': self.input_data['Identifier']}

    def process_response_dict(self, result):
        print 'RemoveProfile.process_response_dict() called'
        if result['Status'] == 'Acknowledged':
            print 'Successfully removed profile identifier:', self.input_data['Identifier']
        else:
            pprint.pprint(result)

class InstallProfile(QueuedMDMCommand):
    request_type = 'InstallProfile'
    def generate_command_dict(self):
        db_profile = db_session.query(DBProfile).filter(DBProfile.id == int(self.input_data['id'])).one()
        return {'Payload': plistlib.Data(db_profile.profile_data)}

    def process_response_dict(self, result):
        print 'InstallProfile.process_response_dict() called'
        if result['Status'] == 'Acknowledged':
            print 'Successfully installed profile id:', self.input_data['id']
        else:
            pprint.pprint(result)

class AppInstall(QueuedMDMCommand):
    request_type = 'InstallApplication'
    def generate_command_dict(self):
        config = db_session.query(MDMConfig).one()

        cmd_dict = {}
        cmd_dict['ManifestURL'] = '%s/app/%d/manifest' % (config.base_url(), self.input_data['id'])
        cmd_dict['Options'] = {'NotManaged': True}
        cmd_dict['ManagementFlags'] = 0

        return cmd_dict

    def process_response_dict(self, result):
        print 'InstallProfile.process_response_dict() called'
        pprint.pprint(result)
