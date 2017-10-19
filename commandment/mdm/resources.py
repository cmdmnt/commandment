from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from commandment.mdm.schema import CommandSchema
from commandment.models import db, Command


class CommandsList(ResourceList):
    schema = CommandSchema
    data_layer = {
        'session': db.session,
        'model': Command,
    }


class CommandDetail(ResourceDetail):
    schema = CommandSchema
    data_layer = {
        'session': db.session,
        'model': Command,
        'url_field': 'command_id'
    }


class CommandRelationship(ResourceRelationship):
    schema = CommandSchema
    data_layer = {'session': db.session, 'model': Command}
