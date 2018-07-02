"""
    This module defines resources, as required by the Flask-REST-JSONAPI package. This represents most of the REST API.
"""
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from .schema import DeviceSchema, CertificateSchema, PrivateKeySchema, \
    CertificateSigningRequestSchema, OrganizationSchema, TagSchema, AvailableOSUpdateSchema
from commandment.models import db, Device, Certificate, CertificateSigningRequest, CACertificate, PushCertificate, \
    SSLCertificate, Organization, Tag, Command
from commandment.inventory.models import AvailableOSUpdate
from commandment.mdm import commands as mdmcommands, CommandType

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship


class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {
        'session': db.session,
        'model': Device,
        'url_field': 'device_id'
    }

    def before_patch(self, args, kwargs, data=None):
        """Custom logic when updating a device:

        - If the `device_name` field would change, we queue a new Settings command to change the name of the device.
        - If there already was an undelivered Settings command, it should be replaced by the new one.
        - If the `hostname` field would change, that should also be sent via a Settings command (will be coalesced with Device Name).
        """
        if 'device_name' in data or 'hostname' in data:
            # settings_commands = self.data_layer['model'].commands
            cmd: mdmcommands.Settings = mdmcommands.Command.new_request_type("Settings", {})

            if 'device_name' in data:
                cmd.device_name = data['device_name']
                del data['device_name']

            if 'hostname' in data:
                cmd.hostname = data['hostname']
                del data['hostname']

            model = Command.from_model(cmd)
            self.data_layer['session'].add(model)


class DeviceRelationship(ResourceRelationship):
    schema = DeviceSchema
    data_layer = {
        'session': db.session,
        'model': Device,
        'url_field': 'device_id'
    }


class CertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateTypeDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class PrivateKeyDetail(ResourceDetail):
    schema = PrivateKeySchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateSigningRequestList(ResourceList):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest,
    }


class CertificateSigningRequestDetail(ResourceDetail):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest
    }


class PushCertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': PushCertificate
    }


class CACertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': CACertificate
    }


class SSLCertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': SSLCertificate
    }


class OrganizationList(ResourceList):
    schema = OrganizationSchema
    data_layer = {
        'session': db.session,
        'model': Organization
    }


class OrganizationDetail(ResourceDetail):
    schema = OrganizationSchema
    data_layer = {
        'session': db.session,
        'model': Organization
    }


class TagsList(ResourceList):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag
    }
    view_kwargs = True


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag,
        'url_field': 'tag_id'
    }


class TagRelationship(ResourceRelationship):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag,
        'url_field': 'tag_id'
    }


class AvailableOSUpdateList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(AvailableOSUpdate)
        if view_kwargs.get('device_id') is not None:
            try:
                self.session.query(Device).filter_by(id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'}, "Device: {} not found".format(view_kwargs['device_id']))
            else:
                query_ = query_.join(Device).filter(Device.id == view_kwargs['device_id'])
        return query_

    schema = AvailableOSUpdateSchema
    view_kwargs = True
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate,
        'methods': {'query': query}
    }


class AvailableOSUpdateDetail(ResourceDetail):
    schema = AvailableOSUpdateSchema
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate,
        'url_field': 'available_os_update_id'
    }


