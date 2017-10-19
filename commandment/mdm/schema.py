from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema


class CommandSchema(Schema):
    class Meta:
        type_ = 'commands'
        self_view = 'api_app.command_detail'
        self_view_kwargs = {'command_id': '<id>'}
        self_view_many = 'api_app.commands_list'
        strict = True

    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    request_type = fields.Str()
    status = fields.Str()
    queued_at = fields.DateTime()
    sent_at = fields.DateTime()
    acknowledged_at = fields.DateTime()
    after = fields.DateTime()
    ttl = fields.Int()

    device = Relationship(
        related_view='api_app.device_detail',
        related_view_kwargs={'device_id': '<id>'},
        type_='devices'
    )

