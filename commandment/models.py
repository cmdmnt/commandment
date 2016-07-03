'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableDict
from .mutablelist import MutableList
from .database import JSONEncodedDict, Base, or_, and_
from profiles.mdm import MDM_AR__ALL

from .pki.x509 import (Certificate as X509Certificate,
                       PrivateKey as X509PrivateKey,
                       CertificateRequest as X509CertificateRequest)

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

certreq_private_key_assoc = Table('certreq_private_key', Base.metadata,
    Column('certreq_id', Integer, ForeignKey('certificate_request.id')),
    Column('privatekey_id', Integer, ForeignKey('rsa_private_key.id')),
)

class PrivateKey(Base):
    __tablename__ = 'rsa_private_key'

    id = Column(Integer, primary_key=True)
    pem_key = Column(Text, nullable=False)

    certificates = relationship('Certificate', secondary=certificate_private_key_assoc, backref='privatekeys')
    certificate_requests = relationship('CertificateRequest', secondary=certreq_private_key_assoc, backref='privatekeys')

    def to_x509(self, key_type=X509PrivateKey):
        return key_type.from_pem(self.pem_key)

    @classmethod
    def from_x509(cls, private_key):
        newcls = cls()
        newcls.pem_key = private_key.to_pem()
        return newcls

class CertificateRequest(Base):
    __tablename__ = 'certificate_request'

    id = Column(Integer, primary_key=True)
    req_type = Column(String(64), nullable=False, index=True) # CERT_TYPES.keys()
    subject = Column(Text, nullable=True)
    pem_request = Column(Text, nullable=False)

    def to_x509(self, request_type=X509CertificateRequest):
        return request_type.from_pem(self.pem_request)

    @classmethod
    def from_x509(cls, req, req_type):
        newcls = cls()
        newcls.subject = req.get_subject_text()
        newcls.req_type = req_type
        newcls.pem_request = req.to_pem()
        return newcls

class Certificate(Base):
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True)
    cert_type = Column(String(64), nullable=False, index=True) # CERT_TYPES.keys()

    subject = Column(Text, nullable=True)

    not_before = Column(DateTime(timezone=False), nullable=False)
    not_after = Column(DateTime(timezone=False), nullable=False)

    # SHA-256 hash of DER-encoded certificate
    fingerprint = Column(String(64), nullable=False, index=True, unique=True) # Unique

    # subject_key_id?
    # auth_key_id?

    # sourced_from = 'scep, self-signed, imported, signed' ?

    pem_certificate = Column(Text, nullable=False)

    @classmethod
    def find_one_by_cert_type(cls, cert_type):
        return cls.query.filter(cls.cert_type == cert_type).one()

    def to_x509(self, cert_type=X509Certificate):
        return cert_type.from_pem(self.pem_certificate)

    @classmethod
    def from_x509(cls, certificate, cert_type):
        newcls = cls()
        newcls.cert_type = cert_type
        newcls.subject = certificate.get_subject_text()
        newcls.not_before = certificate.get_not_before()
        newcls.not_after = certificate.get_not_after()
        newcls.fingerprint = certificate.get_fingerprint('sha256')
        newcls.pem_certificate = certificate.to_pem()
        return newcls

certreq_cert_assoc = Table('certreq_cert', Base.metadata,
    Column('certreq_id', Integer, ForeignKey('certificate_request.id')),
    Column('certificate_id', Integer, ForeignKey('certificate.id')),
)

class InternalCA(Base):
    __tablename__ = 'internal_ca'

    id = Column(Integer, primary_key=True)
    ca_type = Column(String(64), nullable=False, index=True)
    serial = Column(Integer, nullable=False)

    certificate_id = Column(ForeignKey('certificate.id'), unique=True)
    certificate = relationship('Certificate', backref='internalca')

    def get_next_serial(self):
        '''Increment our serial number and return it for use in a 
        new certificate'''

        # MAX(serial) + 1
        pass

internalca_issued_cert_assoc = Table('internalca_issued_cert', Base.metadata,
    Column('certificate_id', Integer, ForeignKey('certificate.id')),
    Column('internalca_id', Integer, ForeignKey('internal_ca.id')),
)

class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)

    udid = Column(String, index=True, nullable=True)
    push_magic = Column(String, nullable=True)
    token = Column(String, nullable=True) # stored as b64-encoded raw data
    unlock_token = Column(String(), nullable=True)
    topic = Column(String, nullable=True)

    serial_number = Column(String(64), index=True, nullable=True)
    dep_json = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True)
    dep_config_id = Column(ForeignKey('dep_config.id'), nullable=True)
    dep_config = relationship('DEPConfig', backref='devices')
    info_json = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True)
    first_user_message_seen = Column(Boolean, nullable=False, default=False)

    certificate_id = Column(ForeignKey('certificate.id'))
    certificate = relationship('Certificate', backref='devices')

    def __repr__(self):
        return '<Device ID=%r UDID=%r SerialNo=%r>' % (self.id, self.udid, self.serial_number)


class QueuedCommand(Base):
    __tablename__ = 'queued_command'

    id = Column(Integer, primary_key=True)

    command_class = Column(String, nullable=False) # string representation of our local command handler
    # request_type = Column(String, index=True, nullable=False) # actual command name
    uuid = Column(String(36), index=True, unique=True, nullable=False)
    input_data = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True) # JSON add'l data as input to command builder
    queued_status = Column(String(1), index=True, nullable=False, default='Q') # 'Q' = Queued, 'S' = Sent
    result = Column(String, index=True, nullable=True) # Status key of MDM command result submission

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

    def set_responded(self):
        self.queued_status = 'R'

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter(cls.uuid == uuid).one()

    @classmethod
    def get_next_device_command(cls, device):
        # d == d AND (q_status == Q OR (q_status == R AND result == 'NotNow'))
        return cls.query.filter(
            and_(cls.device == device,
                or_(cls.queued_status == 'Q',
                    and_(cls.queued_status == 'R',
                        cls.result == 'NotNow')))).order_by(cls.id).first()

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

    def __repr__(self):
        return '<Profile ID=%r UUID=%r>' % (self.id, self.uuid)

device_group_assoc = Table('device_group', Base.metadata,
    Column('mdm_group_id', Integer, ForeignKey('mdm_group.id')),
    Column('device_id', Integer, ForeignKey('device.id')),
)

profile_group_assoc = Table('profile_group', Base.metadata,
    Column('mdm_group_id', Integer, ForeignKey('mdm_group.id')),
    Column('profile_id', Integer, ForeignKey('profile.id')),
)

app_group_assoc = Table('app_group', Base.metadata,
    Column('mdm_group_id', Integer, ForeignKey('mdm_group.id')),
    Column('app_id', Integer, ForeignKey('app.id')),
    # install_early is just a colloqualism to mean 'install as early as
    # possible.' initiallly this is in support for installing apps out of the
    # gate for DEP
    Column('install_early', Boolean),
)

class MDMGroup(Base):
    __tablename__ = 'mdm_group'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    devices = relationship('Device', secondary=device_group_assoc, backref='mdm_groups')
    profiles = relationship('Profile', secondary=profile_group_assoc, backref='mdm_groups')
    apps = relationship('App', secondary=app_group_assoc, backref='mdm_groups')

    def __repr__(self):
        return '<MDMGroup ID=%r Name=%r>' % (self.id, self.group_name)

class MDMConfig(Base):
    __tablename__ = 'mdm_config'

    id = Column(Integer, primary_key=True)

    prefix = Column(String, nullable=False, unique=True)
    addl_config = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True)
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

    # note: we default to 'provide' here despite its lower security because
    # it requires no other dependencies, i.e. a better user experience
    device_identity_method = Column(Enum('ourscep', 'scep', 'provide'), default='provide', nullable=False)
    scep_url = Column(String, nullable=True)
    scep_challenge = Column(String, nullable=True)

    def base_url(self):
        # yuck, since we don't actually save the base URL in our MDMConfig we'll
        # have to compute it from the MDM URL by stripping off the trailing "/mdm"
        if self.mdm_url[-4:] == '/mdm':
            return self.mdm_url[:-4]
        else:
            return ''

class SCEPConfig(Base):
    __tablename__ = 'scep_config'

    id = Column(Integer, primary_key=True)
    challenge = Column(String, nullable=False)

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

    bundle_ids_json = Column(MutableList.as_mutable(JSONEncodedDict), nullable=True)
    pkg_ids_json = Column(MutableList.as_mutable(JSONEncodedDict), nullable=True)

    def path_format(self):
        return '%010d.dat' % self.id

    def __repr__(self):
        return '<App ID=%r Filename=%r>' % (self.id, self.filename)

class DEPConfig(Base):
    __tablename__ = 'dep_config'

    id = Column(Integer, primary_key=True)

    # certificate for PKI of server token
    certificate_id = Column(ForeignKey('certificate.id'))
    certificate = relationship('Certificate', backref='dep_configs')

    server_token = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True)
    auth_session_token = Column(String, nullable=True)

    initial_fetch_complete = Column(Boolean, nullable=False, default=False)
    next_check = Column(DateTime(timezone=False), nullable=True)
    device_cursor = Column(String)
    device_cursor_recevied = Column(DateTime(timezone=False), nullable=True) # shouldn't use if more than 7 days old

    url_base = Column(String, nullable=True) # testing server environment if used

    def last_check_delta(self):
        if self.next_check:
            return str(self.next_check - datetime.datetime.utcnow())
        else:
            return ''

class DEPProfile(Base):
    __tablename__ = 'dep_profile'

    id = Column(Integer, primary_key=True)

    mdm_config_id = Column(ForeignKey('mdm_config.id'), nullable=False)
    mdm_config = relationship('MDMConfig', backref='dep_profiles')

    dep_config_id = Column(ForeignKey('dep_config.id'), nullable=False)
    dep_config = relationship('DEPConfig', backref='dep_profiles')

    # DEP-assigned UUID for this DEP profile
    uuid = Column(String(36), index=True, nullable=True) # should be unique but it's assigned to us so can't be null

    profile_data = Column(MutableDict.as_mutable(JSONEncodedDict), nullable=False)

    def profile_name(self):
        return self.profile_data['profile_name']
