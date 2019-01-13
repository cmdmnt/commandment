from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.apps.schema import ApplicationManifestSchema, ApplicationSchema, ManagedApplicationSchema
from commandment.apps.models import db, ApplicationManifest, Application, ManagedApplication, AppstoreMacApplication, \
    AppstoreiOSApplication, EnterpriseMacApplication, EnterpriseiOSApplication


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


class MASApplicationDetail(ResourceDetail):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': AppstoreMacApplication,
        'url_field': 'application_id'
    }


class MASApplicationList(ResourceList):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': AppstoreMacApplication,
        'url_field': 'application_id'
    }


class IOSApplicationDetail(ResourceDetail):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': AppstoreiOSApplication,
        'url_field': 'application_id'
    }


class IOSApplicationList(ResourceList):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': AppstoreiOSApplication,
        'url_field': 'application_id'
    }


class EnterpriseMacApplicationList(ResourceList):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': EnterpriseMacApplication,
        'url_field': 'application_id'
    }


class EnterpriseMacApplicationDetail(ResourceDetail):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': EnterpriseMacApplication,
        'url_field': 'application_id'
    }


class EnterpriseIosApplicationList(ResourceList):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': EnterpriseiOSApplication,
        'url_field': 'application_id'
    }


class EnterpriseIosApplicationDetail(ResourceDetail):
    schema = ApplicationSchema
    data_layer = {
        'session': db.session,
        'model': EnterpriseiOSApplication,
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
