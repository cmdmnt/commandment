from marshmallow import Schema, fields


class Profile(Schema):
    profile_name = fields.String()
    url = fields.Url()
    allow_pairing = fields.Boolean()
    is_supervised = fields.Boolean()
    is_multi_user = fields.Boolean()
    is_mandatory = fields.Boolean()
    await_device_configured = fields.Boolean()
    is_mdm_removable = fields.Boolean()
    support_phone_number = fields.String()
    auto_advance_setup = fields.Boolean()
    support_email_address = fields.Email()
    org_magic = fields.String()
    anchor_certs = fields.List(fields.String())
    supervising_host_certs = fields.List(fields.String())
    skip_setup_items = fields.String()