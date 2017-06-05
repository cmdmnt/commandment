from marshmallow import Schema, fields


class ProfileRequest(Schema):
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
    department = fields.String()
    devices = fields.List(fields.String())


class Device(Schema):
    """The Device dictionary returned by the DEP Devices fetch endpoint.

    See Also:
          https://mdmenrollment.apple.com/server/devices
    """
    serial_number = fields.String()
    model = fields.String()
    description = fields.String()
    color = fields.String()
    asset_tag = fields.String()
    profile_status = fields.String()
    profile_uuid = fields.UUID()
    profile_assign_time = fields.DateTime()
    profile_push_time = fields.DateTime()
    device_assigned_date = fields.DateTime()
    device_assigned_by = fields.Email()
    os = fields.String()
    device_family = fields.String()


class MDMServiceURL(Schema):
    uri = fields.URL()
    http_method = fields.String()
    # limit


class AccountDetails(Schema):
    """DEP Account Details"""
    server_name = fields.String()
    server_uuid = fields.UUID()
    admin_id = fields.Email()
    org_name = fields.String()
    org_email = fields.Email()
    org_phone = fields.String()
    org_address = fields.String()
    urls = fields.Nested(MDMServiceURL, many=True)
    org_type = fields.String()
    org_version = fields.String()
    org_id = fields.String()
    org_id_hash = fields.String()
