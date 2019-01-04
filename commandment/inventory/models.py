from sqlalchemy.ext.mutable import MutableList

from commandment.models import db
from commandment.dbtypes import GUID, JSONEncodedDict


class InstalledApplication(db.Model):
    """This model represents a single application that was returned as part of an ``InstalledApplicationList`` query.

    It is impossible to create a composite key to uniquely identify each row, therefore every time the device reports
    back we need to wipe all rows associated with a single device. The reason why a composite key won't work here is
    that macOS will often report the binary name and no identifier, version, or size (and sometimes iOS can do the
    inverse of that).

    :table: installed_applications

    See Also:
          - `InstalledApplicationList Command <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/3-MDM_Protocol/MDM_Protocol.html#//apple_ref/doc/uid/TP40017387-CH3-SW14>`_.
    """
    __tablename__ = 'installed_applications'

    id = db.Column(db.Integer, primary_key=True)
    """id (int): Identifier"""
    device_udid = db.Column(db.String(40), index=True, nullable=False)
    """device_udid (GUID): Unique device identifier"""
    device_id = db.Column(db.ForeignKey('devices.id'), nullable=True)
    """device_id (int): Parent relationship ID of the device"""
    device = db.relationship('Device', backref='installed_applications')
    """device (db.relationship): SQLAlchemy relationship to the device."""

    # Many of these can be empty, so there is no valid composite key
    bundle_identifier = db.Column(db.String, index=True)
    """bundle_identifier (str): The com.xxx.yyy bundle identifier for the application. May be empty."""
    version = db.Column(db.String, index=True)
    """version (str): The long version for the application. May be empty."""
    short_version = db.Column(db.String)
    """short_version (str): The short version for the application. May be empty."""
    name = db.Column(db.String)
    """name (str): The application name"""
    bundle_size = db.Column(db.BigInteger)
    """bundle_size (int): The application size"""
    dynamic_size = db.Column(db.BigInteger)
    """dynamic_size (int): The dynamic data size (for iOS containers)."""
    is_validated = db.Column(db.Boolean)
    """is_validated (bool):"""
    external_version_identifier = db.Column(db.BigInteger, index=True)
    """external_version_identifier (int): The application’s external version ID. 
       It can be used for comparison in the iTunes Search API to decide if the application needs to be updated."""
    adhoc_codesigned = db.Column(db.Boolean)
    appstore_vendable = db.Column(db.Boolean)
    beta_app = db.Column(db.Boolean)
    device_based_vpp = db.Column(db.Boolean)
    has_update_available = db.Column(db.Boolean)
    installing = db.Column(db.Boolean)


class InstalledCertificate(db.Model):
    """This model represents a single installed certificate on an enrolled device as returned by the ``CertificateList``
    query.

    The response will usually include both certificates managed by profiles and certificates that were installed
    outside of a profile.

    :table: installed_certificates

    See Also:
          - `CertificateList Command <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/3-MDM_Protocol/MDM_Protocol.html#//apple_ref/doc/uid/TP40017387-CH3-SW13>`_.
    """
    __tablename__ = 'installed_certificates'

    id = db.Column(db.Integer, primary_key=True)
    """(int): Installed Certificate ID"""
    device_udid = db.Column(db.String(40), index=True, nullable=False)
    """(GUID): Unique Device Identifier"""
    device_id = db.Column(db.ForeignKey('devices.id'), nullable=True)
    """(int): Device foreign key ID."""
    device = db.relationship('Device', backref='installed_certificates')
    """(db.relationship): Device relationship"""
    x509_cn = db.Column(db.String)
    """(str): The X.509 Common Name of the certificate."""
    is_identity = db.Column(db.Boolean)
    """(bool): Is the certificate an identity certificate?"""
    der_data = db.Column(db.LargeBinary, nullable=False)
    """(bytes): The DER encoded certificate data."""
    fingerprint_sha256 = db.Column(db.String(64), nullable=False, index=True)
    """(str): SHA-256 fingerprint of the certificate."""


class InstalledProfile(db.Model):
    """This model represents a single installed profile on an enrolled device as returned by the ``ProfileList`` query.

    The response does not contain the entire contents of the profiles installed therefore the UUIDs returned are joined
    against our profiles table to ascertain whether profiles have been installed or not.

    :table: installed_profiles

    See Also:
          - `ProfileList Command <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/3-MDM_Protocol/MDM_Protocol.html#//apple_ref/doc/uid/TP40017387-CH3-SW7>`_.
    """
    __tablename__ = 'installed_profiles'

    id = db.Column(db.Integer, primary_key=True)
    """(int): Installed Profile ID"""
    device_udid = db.Column(db.String(40), index=True, nullable=False)
    """(GUID): Unique Device Identifier"""
    device_id = db.Column(db.ForeignKey('devices.id'), nullable=True)
    """(int): Device foreign key ID."""
    device = db.relationship('Device', backref='installed_profiles')
    """(db.relationship): Device relationship"""

    has_removal_password = db.Column(db.Boolean)
    """(bool): Does the installed profile have a removal password?"""
    is_encrypted = db.Column(db.Boolean)
    """(bool): Is the installed profile encrypted?"""
    is_managed = db.Column(db.Boolean)
    """(bool): Is the installed profile managed? which means it has been sourced from the MDM."""

    payload_description = db.Column(db.String)
    """(str): Payload description (value of PayloadDescription)"""
    payload_display_name = db.Column(db.String)
    """(str): Payload display name"""
    payload_identifier = db.Column(db.String)
    payload_organization = db.Column(db.String)
    payload_removal_disallowed = db.Column(db.Boolean)
    payload_uuid = db.Column(GUID, index=True)
    # SignerCertificates


class InstalledPayload(db.Model):
    __tablename__ = 'installed_payloads'

    id = db.Column(db.Integer, primary_key=True)
    """(int): Installed Payload ID"""
    profile_id = db.Column(db.ForeignKey('installed_profiles.id'), nullable=False)
    """(int): InstalledProfile foreign key ID."""
    profile = db.relationship('InstalledProfile', backref='payload_content')
    device_id = db.Column(db.ForeignKey('devices.id'), nullable=True)
    """(int): Device foreign key ID."""
    device = db.relationship('Device', backref='installed_payloads')
    """(db.relationship): Device relationship"""

    """(db.relationship): InstalledProfile relationship"""
    description = db.Column(db.String)
    """(str): Payload description (value of PayloadDescription)"""
    display_name = db.Column(db.String)
    """(str): Payload display name"""
    identifier = db.Column(db.String)
    organization = db.Column(db.String)
    payload_type = db.Column(db.String)
    uuid = db.Column(GUID())


class AvailableOSUpdate(db.Model):
    """This table holds the results of `AvailableOSUpdates` commands."""
    __tablename__ = 'available_os_updates'

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(db.ForeignKey('devices.id'), nullable=True)
    """(int): Device foreign key ID."""
    device = db.relationship('Device', backref='available_os_updates')
    """(db.relationship): Device relationship"""

    # Common to all platforms
    allows_install_later = db.Column(db.Boolean)
    human_readable_name = db.Column(db.String)
    is_critical = db.Column(db.Boolean)
    product_key = db.Column(db.String)
    restart_required = db.Column(db.Boolean)
    version = db.Column(db.String)

    # macOS Only
    app_identifiers_to_close = db.Column(MutableList.as_mutable(JSONEncodedDict))
    human_readable_name_locale = db.Column(db.String)
    is_config_data_update = db.Column(db.Boolean)
    """(bool): This update is a config data update eg. for XProtect or Gatekeeper. These arent normally shown"""
    is_firmware_update = db.Column(db.Boolean)
    metadata_url = db.Column(db.String)

    # iOS Only
    product_name = db.Column(db.String)
    build = db.Column(db.String)
    download_size = db.Column(db.BigInteger)
    install_size = db.Column(db.BigInteger)
