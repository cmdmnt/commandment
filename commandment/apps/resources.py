from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.apps.schema import ApplicationManifestSchema, ApplicationSchema, ManagedApplicationSchema
from commandment.apps.models import db, ApplicationManifest, Application, ManagedApplication


class ApplicationManifestDetail(ResourceDetail):
    schema = ApplicationManifestSchema
    data_layer = {
        'session': db.session,
        'model': ApplicationManifest,
        'url_field': 'application_manifest_id'
    }


class ApplicationDetail(ResourceDetail):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': Application,
        'url_field': 'application_id'
    }


class ApplicationList(ResourceList):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': Application,
        'url_field': 'application_id'
    }


class ApplicationRelationship(ResourceRelationship):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': Application,
        'url_field': 'application_id'
    }


class ManagedApplicationDetail(ResourceDetail):
    schema = ManagedApplicationSchema
    data_layer = {
        'session': db.session,
        'model': ManagedApplication,
        'url_field': 'managed_application_id',
    }


class ManagedApplicationList(ResourceList):
    schema = ManagedApplicationSchema
    data_layer = {
        'session': db.session,
        'model': ManagedApplication,
        'url_field': 'managed_application_id',
    }


class ManagedApplicationRelationship(ResourceRelationship):
    schema = ManagedApplicationSchema
    data_layer = {
        'session': db.session,
        'model': ManagedApplication,
        'url_field': 'managed_application_id',
    }
