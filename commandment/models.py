'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from .database import JSONEncodedDict, Base
from profiles.mdm import MDM_AR__ALL

CERT_TYPES = {
    'mdm.pushcert': {
        'title': 'APNS MDM Push Certificate',
        'description': 'Used to send MDM push notifications to devices using APNS',
        'required': True,
        'pkey_required': True,
    },
    'mdm.webcrt': {
        'title': 'MDM Web Server Certificate',
        'description': 'Used to install as trusted root on MDM devices to trust web URL of MDM system',
        'required': False,
        'pkey_required': False,
    },
    'mdm.cacert': {
        'title': 'MDM Certificate Authority Root Certificate',
        'description': 'Used to sign individual device enrollment certificates',
        'required': True,
        'pkey_required': True,
    },
    'mdm.device': {
        'title': 'Per-device client certificate',
        'description': 'MDM-enrolled device authentication/identification certificate issued by MDM CA',
        'required': False,
        'pkey_required': False,
    },
}

certificate_private_key_assoc = Table('certificate_private_key', Base.metadata,
    Column('certificate_id', Integer, ForeignKey('certificate.id')),
    Column('privatekey_id', Integer, ForeignKey('rsa_private_key.id')),
)

class PrivateKey(Base):
    __tablename__ = 'rsa_private_key'

    id = Column(Integer, primary_key=True)
    pem_key = Column(Text)

    certificates = relationship('Certificate', secondary=certificate_private_key_assoc, backref='privatekeys')

class Certificate(Base):
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True)
    cert_type = Column(String(64), index=True)
    pem_certificate = Column(Text, index=True)

    @classmethod
    def find_one_by_cert_type(cls, cert_type):
        return cls.query.filter(cls.cert_type == cert_type).one()



class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)

    udid = Column(String, unique=True, index=True, nullable=False)
    push_magic = Column(String, nullable=True)
    token = Column(String, nullable=True)
    unlock_token = Column(String(), nullable=True)
    topic = Column(String, nullable=True)

    info_json = Column(JSONEncodedDict, nullable=True)

    certificate_id = Column(ForeignKey('certificate.id'))
    certificate = relationship('Certificate', backref='devices')

    def __repr__(self):
        return '<Device ID=%r UDID=%r>' % (self.id, self.udid)


class QueuedCommand(Base):
    __tablename__ = 'queued_command'

    id = Column(Integer, primary_key=True)

    command_class = Column(String, nullable=False) # string representation of our local command handler
    uuid = Column(String(36), index=True, unique=True, nullable=False)
    input_data = Column(JSONEncodedDict, nullable=True) # JSON add'l data as input to command builder
    queued_status = Column(String(1), index=True, nullable=False, default='Q') # 'Q' = Queued, 'S' = Sent
    result = Column(String, nullable=True)

    # queued_stamp
    # sent_stamp
    # result_stamp

    device_id = Column(ForeignKey('device.id'), nullable=False)
    device = relationship('Device', backref='queued_command')

    def set_sent(self):
        self.queued_status = 'S'

    def set_processing(self):
        self.queued_status = 'P'

    def set_invalid(self):
        self.queued_status = 'X'

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter(cls.uuid == uuid).one()

    @classmethod
    def get_next_device_command(cls, device):
        # TODO: order_by queued_stamp
        return cls.query.filter(cls.device == device, cls.queued_status == 'Q').first()

    def __repr__(self):
        return '<QueuedCommand ID=%r UUID=%r qstatus=%r>' % (self.id, self.uuid, self.queued_status)

# profile_device_assoc = Table('profile_device', Base.metadata,
#   Column('device_id', Integer, ForeignKey('device.id')),
#   Column('profile_id', Integer, ForeignKey('profile.id')),
# )

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    identifier = Column(String, index=True, unique=True, nullable=False) # duplicated from within profile_data for searching
    uuid = Column(String(36), index=True, unique=True, nullable=False) # duplicated from within profile_data for searching
    profile_data = Column(Text, nullable=False) # serialized XML (or signed, encrypted) profile data

device_group_assoc = Table('device_group', Base.metadata,
    Column('mdm_group_id', Integer, ForeignKey('mdm_group.id')),
    Column('device_id', Integer, ForeignKey('device.id')),
)

profile_group_assoc = Table('profile_group', Base.metadata,
    Column('mdm_group_id', Integer, ForeignKey('mdm_group.id')),
    Column('profile_id', Integer, ForeignKey('profile.id')),
)

class MDMGroup(Base):
    __tablename__ = 'mdm_group'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    devices = relationship('Device', secondary=device_group_assoc, backref='mdm_groups')
    profiles = relationship('Profile', secondary=profile_group_assoc, backref='mdm_groups')

class MDMConfig(Base):
    __tablename__ = 'mdm_config'

    id = Column(Integer, primary_key=True)

    prefix = Column(String, nullable=False, unique=True)
    addl_config = Column(JSONEncodedDict, nullable=True)
    topic = Column(String, nullable=False) # APNs Push Topic
    access_rights = Column(Integer, default=MDM_AR__ALL, nullable=False)

    mdm_url = Column(String, nullable=False)
    checkin_url = Column(String, nullable=False)

    mdm_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    ca_cert_id = Column(ForeignKey('certificate.id'))
    ca_cert = relationship('Certificate', foreign_keys=[ca_cert_id]) # , backref='ca_cert_mdm_config'

    push_cert_id = Column(ForeignKey('certificate.id'), nullable=False)
    push_cert = relationship('Certificate', foreign_keys=[push_cert_id]) # , backref='push_cert_mdm_config'

class App(Base):
    __tablename__ = 'app'

    id = Column(Integer, primary_key=True)

    filename = Column(String, nullable=False, unique=True)
    filesize = Column(Integer, nullable=False)

    md5_hash = Column(String(32), nullable=False) # MD5 hash of the entire file

    # MDM clients support a chunked method of retrival of the download file
    # presumably to best support OTA download of large updates. These fields
    # are in support of that mechanism
    md5_chunk_size = Column(Integer, nullable=False)
    md5_chunk_hashes = Column(Text, nullable=True) # colon (:) separated list of MD5 chunk hashes

    bundle_ids_json = Column(JSONEncodedDict, nullable=True)
    pkg_ids_json = Column(JSONEncodedDict, nullable=True)

    def path_format(self):
        return '%010d.dat' % self.id
