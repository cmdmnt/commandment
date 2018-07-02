from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from commandment.mdm.schema import CommandSchema
from commandment.models import db, Command, Device


class CommandsList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Command)
        if view_kwargs.get('device_id') is not None:
            try:
                self.session.query(Device).filter_by(id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'}, "Device: {} not found".format(view_kwargs['device_id']))
            else:
                query_ = query_.join(Device).filter(Device.id == view_kwargs['device_id'])
        return query_

    schema = CommandSchema
    view_kwargs = True
    data_layer = {
        'session': db.session,
        'model': Command,
        'methods': {'query': query}
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
