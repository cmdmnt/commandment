'''
Copyright (c) 2016 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from . import QueuedMDMCommand
from passlib.hash import pbkdf2_sha512
from passlib.utils.handlers import validate_secret
import biplist
import plistlib

class osx_pbkdf2_sha512(pbkdf2_sha512):
    checksum_size = 128
    default_salt_size = 32
    min_rounds = 20000
    max_rounds = 40000
    default_rounds = 30000
    # referenced only once in passlib/handlers/pbkdf2.py
    encoded_checksum_size = (128 * 4 + 2) // 3

    @classmethod
    def hash_to_dep_biplist(cls, secret, config=None, **kwds):
        validate_secret(secret)
        self = cls(use_defaults=True, **kwds)
        self.checksum = self._calc_checksum(secret)

        plist_dict = {
            'SALTED-SHA512-PBKDF2': {
                'entropy': biplist.Data(self.checksum),
                'salt': biplist.Data(self.salt),
                'iterations': int(self.rounds),
            }
        }

        return biplist.writePlistToString(plist_dict)

class AdminAccountTest(QueuedMDMCommand):
    request_type = 'AccountConfiguration'

    def generate_command_dict(self):
        cmd_dict = {}

        # cmd_dict['SkipPrimarySetupAccountCreation'] = True # default False
        # cmd_dict['SetPrimarySetupAccountAsRegularUser'] = False # default False

        account = {
            'shortName': 'firstboot',
            'fullName': 'password is "password"',
            'passwordHash': plistlib.Data(
                osx_pbkdf2_sha512.hash_to_dep_biplist('password')),
            'hidden': False,
        }
        cmd_dict['AutoSetupAdminAccounts'] = [account]

        return cmd_dict

    def process_response_dict(self, result):
        pass

class DeviceConfigured(QueuedMDMCommand):
    request_type = 'DeviceConfigured'
    def generate_command_dict(self):
        return {}
    def process_response_dict(self, result):
        pass
