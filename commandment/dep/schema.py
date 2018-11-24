from flask import url_for
from marshmallow_jsonapi.flask import Relationship, Schema
from marshmallow_jsonapi import fields
from marshmallow_enum import EnumField
from . import SetupAssistantStep


class DEPProfileSchema(Schema):
    """marshmallow schema for a DEP profile.

    See Also:
        - `/profile endpoint <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW6>`_.
        - `Mobile Device Management Protocol Reference <https://developer.apple.com/enterprise/documentation/MDM-Protocol-Reference.pdf>`_ "Define Profile" pg. 120
    """
    class Meta:
        type_ = 'dep_profiles'
        self_view = 'dep_app.dep_profile_detail'
        self_view_kwargs = {'dep_profile_id': '<id>'}
        self_view_many = 'dep_app.dep_profiles_list'
        strict = True

    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    """str: The Apple assigned UUID of this DEP Profile"""

    profile_name = fields.String(required=True)
    """str: A human-readable name for the profile."""
    url = fields.Url(required=False)  # Should be required
    """str: The URL of the MDM server."""
    allow_pairing = fields.Boolean(default=True)
    """bool: If true, any device can pair with this device, supervision certs are not required."""
    is_supervised = fields.Boolean(default=False)
    """bool: If true, the device must be supervised"""
    is_multi_user = fields.Boolean(default=False)
    """bool: If true, tells the device to configure for Shared iPad."""
    is_mandatory = fields.Boolean(default=False)
    """bool: If true, the user may not skip applying the profile returned by the MDM server"""
    await_device_configured = fields.Boolean()
    """bool: If true, Setup Assistant does not continue until the MDM server sends DeviceConfigured."""
    is_mdm_removable = fields.Boolean()
    """bool: If false, the MDM payload delivered by the configuration URL cannot be removed by the user via the user 
    interface on the device"""
    support_phone_number = fields.String(allow_none=True)
    """str: A support phone number for the organization."""
    auto_advance_setup = fields.Boolean()
    """bool: If set to true, the device will tell tvOS Setup Assistant to automatically advance though its screens."""
    support_email_address = fields.String(allow_none=True)  # No need to perform validation here
    """str: A support email address for the organization."""
    org_magic = fields.String(allow_none=True)
    """str: A string that uniquely identifies various services that are managed by a single organization."""
    anchor_certs = fields.List(fields.String())
    """List[str]: Each string should contain a DER-encoded certificate converted to Base64 encoding. If provided, 
    these certificates are used as trusted anchor certificates when evaluating the trust of the connection 
    to the MDM server URL."""
    supervising_host_certs = fields.List(fields.String())
    """List[str]: Each string contains a DER-encoded certificate converted to Base64 encoding. If provided, 
    the device will continue to pair with a host possessing one of these certificates even when allow_pairing 
    is set to false"""
    skip_setup_items = fields.List(EnumField(SetupAssistantStep))
    """Set[SetupAssistantStep]: A list of setup panes to skip"""
    department = fields.String(allow_none=True)
    """str: The user-defined department or location name."""
    last_upload_at = fields.DateTime(dump_only=True)
    """datetime: The last time this profile was uploaded/synced to apple. null if it was never synced."""

    devices = Relationship(
        related_view='api_app.devices_list',
        related_view_kwargs={'dep_profile_id': '<id>'},
        many=True, include_resource_linkage=True,
        schema='DeviceSchema',
        type_='devices'
    )

    dep_account = Relationship(
        self_view='dep_app.dep_profile_dep_account',
        self_view_kwargs={'dep_profile_id': '<id>'},
        related_view='dep_app.dep_account_detail',
        related_view_kwargs={'dep_account_id': '<dep_account_id>'},
        many=False, include_resource_linkage=True,
        schema='DEPAccountSchema',
        type_='dep_accounts'
    )


class DEPDeviceSchema(Schema):
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


class DEPDeviceSyncSchema(Schema):
    """The device dictionary returned by the DEP Devices sync endpoint.

    This adds the operation type and date."""
    op_type = fields.String()
    op_date = fields.DateTime()
    

class DEPDeviceCursorSchema(Schema):
    """The response JSON literal of the device fetch endpoint"""
    cursor = fields.String()
    more_to_follow = fields.Boolean()
    devices = fields.Nested(DEPDeviceSchema, many=True)
    fetched_until = fields.DateTime()


class MDMServiceURL(Schema):
    uri = fields.URL()
    http_method = fields.String()
    # limit


class DEPAccountSchema(Schema):
    """DEP Account Details"""
    class Meta:
        type_ = 'dep_accounts'
        self_view = 'dep_app.dep_account_detail'
        self_view_kwargs = {'dep_account_id': '<id>'}
        self_view_many = 'dep_app.dep_accounts_list'
        strict = True

    id = fields.Int(dump_only=True)

    # stoken
    consumer_key = fields.String()
    consumer_secret = fields.String(load_only=True)
    access_token = fields.String()
    access_secret = fields.String(load_only=True)
    access_token_expiry = fields.DateTime(dump_only=True)
    token_updated_at = fields.DateTime(dump_only=True)
    auth_session_token = fields.String(load_only=True)

    # org
    server_name = fields.String()
    server_uuid = fields.UUID()
    admin_id = fields.String()
    facilitator_id = fields.String()
    org_name = fields.String()
    org_email = fields.Email()
    org_phone = fields.String()
    org_address = fields.String()
    # urls = fields.Nested(MDMServiceURL, many=True)
    org_type = fields.String()
    org_version = fields.String()
    org_id = fields.String()
    org_id_hash = fields.String()
    url = fields.String()

    cursor = fields.String()
    more_to_follow = fields.Boolean()
    fetched_until = fields.DateTime()

    dep_profiles = Relationship(
        related_view='dep_app.dep_profile_detail',
        related_view_kwargs={'dep_profile_id': '<id>'},
        many=True, include_resource_linkage=True,
        schema='DEPProfileSchema',
        type_='dep_profiles'
    )
