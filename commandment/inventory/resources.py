from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.inventory.schema import InstalledApplicationSchema, InstalledCertificateSchema, InstalledProfileSchema
from commandment.inventory.models import db, InstalledApplication, InstalledCertificate, InstalledProfile


class InstalledApplicationsList(ResourceList):
    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication
    }


class InstalledApplicationDetail(ResourceDetail):
    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication
    }


class InstalledCertificatesList(ResourceList):
    schema = InstalledCertificateSchema
    data_layer = {
        'session': db.session,
        'model': InstalledCertificate
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
    schema = InstalledProfileSchema
    data_layer = {
        'session': db.session,
        'model': InstalledProfile
    }


class InstalledProfileDetail(ResourceDetail):
    schema = InstalledProfileSchema
    data_layer = {
        'session': db.session,
        'model': InstalledProfile
    }

