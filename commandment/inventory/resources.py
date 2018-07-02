from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from commandment.inventory.schema import InstalledApplicationSchema, InstalledCertificateSchema, \
    InstalledProfileSchema, AvailableOSUpdateSchema
from commandment.inventory.models import db, InstalledApplication, InstalledCertificate, InstalledProfile, \
    AvailableOSUpdate
from commandment.models import Device


class InstalledApplicationsList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(InstalledApplication)
        if view_kwargs.get('device_id') is not None:
            try:
                self.session.query(Device).filter_by(id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'}, "Device: {} not found".format(view_kwargs['device_id']))
            else:
                query_ = query_.join(Device).filter(Device.id == view_kwargs['device_id'])
        return query_

    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication,
        'methods': {'query': query}
    }


class InstalledApplicationDetail(ResourceDetail):
    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication
    }


class InstalledCertificatesList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(InstalledCertificate)
        if view_kwargs.get('device_id') is not None:
            try:
                self.session.query(Device).filter_by(id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'}, "Device: {} not found".format(view_kwargs['device_id']))
            else:
                query_ = query_.join(Device).filter(Device.id == view_kwargs['device_id'])
        return query_

    schema = InstalledCertificateSchema
    view_kwargs = True
    data_layer = {
        'session': db.session,
        'model': InstalledCertificate,
        'methods': {'query': query}
    }


class InstalledCertificateDetail(ResourceDetail):
    schema = InstalledCertificateSchema
    data_layer = {
        'session': db.session,
        'model': InstalledCertificate,
        'url_field': 'installed_certificate_id'
    }


# class PayloadsList(ResourceList):
#     schema = PayloadSchema
#     data_layer = {
#         'session': db.session,
#         'model': Payload
#     }
#
#
# class PayloadDetail(ResourceDetail):
#     schema = PayloadSchema
#     data_layer = {
#         'session': db.session,
#         'model': Payload
#     }

class InstalledProfilesList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(InstalledProfile)
        if view_kwargs.get('device_id') is not None:
            try:
                self.session.query(Device).filter_by(id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'}, "Device: {} not found".format(view_kwargs['device_id']))
            else:
                query_ = query_.join(Device).filter(Device.id == view_kwargs['device_id'])
        return query_

    schema = InstalledProfileSchema
    view_kwargs = True
    data_layer = {
        'session': db.session,
        'model': InstalledProfile,
        'methods': {'query': query}
    }


class InstalledProfileDetail(ResourceDetail):
    schema = InstalledProfileSchema
    data_layer = {
        'session': db.session,
        'model': InstalledProfile
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
