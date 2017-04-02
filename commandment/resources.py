from .schema import DeviceSchema, CertificateSchema, PrivateKeySchema, \
    CertificateSigningRequestSchema, OrganizationSchema
from .models import db, Device, Certificate, CertificateSigningRequest, CACertificate, PushCertificate, \
    SSLCertificate, Organization

from flask_rest_jsonapi import ResourceDetail, ResourceList


class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


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
