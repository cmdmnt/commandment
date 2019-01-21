from sqlalchemy.orm.exc import NoResultFound
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
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
    def query(self, view_kwargs):
        query_ = self.session.query(ManagedApplication)
        if view_kwargs.get('application_id') is not None:
            try:
                self.session.query(Application).filter_by(id=view_kwargs['application_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'application_id'},
                                     "Application: {} not found".format(view_kwargs['application_id']))
            else:
                query_ = query_.join(Application).filter(Application.id == view_kwargs['application_id'])
        return query_

    schema = ManagedApplicationSchema
    data_layer = {
        'session': db.session,
        'model': ManagedApplication,
        'url_field': 'managed_application_id',
        'methods': {'query': query},
    }


class ManagedApplicationRelationship(ResourceRelationship):
    schema = ManagedApplicationSchema
    data_layer = {
        'session': db.session,
        'model': ManagedApplication,
        'url_field': 'managed_application_id',
    }
