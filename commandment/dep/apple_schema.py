from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from . import SetupAssistantStep


class AppleDEPProfileSchema(Schema):
    """marshmallow schema for a DEP profile.

    See Also:
        - `/profile endpoint <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/4-Profile_Management/ProfileManagement.html#//apple_ref/doc/uid/TP40017387-CH7-SW6>`_.
        - `Mobile Device Management Protocol Reference <https://developer.apple.com/enterprise/documentation/MDM-Protocol-Reference.pdf>`_ "Define Profile" pg. 120
    """
    # uuid = fields.UUID(dump_only=True)
    # """str: The Apple assigned UUID of this DEP Profile"""

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
