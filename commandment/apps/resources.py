from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.apps.jsonapi_schema import ApplicationManifestSchema
from commandment.apps.models import db, ApplicationManifest


class ApplicationManifestDetail(ResourceDetail):
    schema = ApplicationManifestSchema
    data_layer = {
        'session': db.session,
        'model': ApplicationManifest,
        'url_field': 'application_manifest_id'
    }
