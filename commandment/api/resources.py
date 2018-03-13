"""
    This module defines resources, as required by the Flask-REST-JSONAPI package. This represents most of the REST API.
"""

from .schema import DeviceSchema, CertificateSchema, PrivateKeySchema, \
    CertificateSigningRequestSchema, OrganizationSchema, TagSchema, AvailableOSUpdateSchema
from commandment.models import db, Device, Certificate, CertificateSigningRequest, CACertificate, PushCertificate, \
    SSLCertificate, Organization, Tag, AvailableOSUpdate

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
    schema = AvailableOSUpdateSchema
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate
    }


class AvailableOSUpdateDetail(ResourceDetail):
    schema = AvailableOSUpdateSchema
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate,
        'url_field': 'available_os_update_id'
    }


