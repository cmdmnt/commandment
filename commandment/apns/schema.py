from marshmallow import Schema, fields


class PushResponseFlatSchema(Schema):
    """This structure mimics the fields of an APNS2 service reply."""
    apns_id = fields.Integer()
    status_code = fields.Integer()
    reason = fields.Str()
    timestamp = fields.DateTime()

