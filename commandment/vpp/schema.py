from marshmallow import Schema, fields


class VPPAccountSchema(Schema):
    exp_date = fields.DateTime()
    org_name = fields.String()
