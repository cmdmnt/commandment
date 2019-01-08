from enum import Enum, IntEnum, IntFlag
from ..models import db


class ManagementFlag(IntFlag):
    """This enum of integer bitwise OR flags represents all the fields available as part of the ``ManagementFlag``
    option to the ``InstallApplication`` command."""
    NOTHING = 0
    REMOVE_APP_WITH_ENROLLMENT = 1
    PREVENT_APPDATA_BACKUP = 4


class PurchaseMethod(IntEnum):
    """Purchase methods, the flag should almost always be VPP_APP_ASSIGNMENT"""
    LEGACY_VPP = 0
    VPP_APP_ASSIGNMENT = 1


class ApplicationType(Enum):
    """A list of the polymorphic identities available for subclasses of Application."""
    ENTERPRISE_MAC = 'enterprise_mac'
    ENTERPRISE_IOS = 'enterprise_ios'
    APPSTORE_MAC = 'appstore_mac'
    APPSTORE_IOS = 'appstore_ios'


application_tags = db.Table(
    'application_tags',
    db.metadata,
    db.Column('application_id', db.Integer, db.ForeignKey('applications.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
)


class Application(db.Model):
    """This table holds details of each individual application that may be
     managed (either app store or enterprise application).

    :table: applications
    """
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    """id (db.Integer): ID"""
    display_name = db.Column(db.String, nullable=False)
    """display_name (db.String): The name of the application displayed in the MDM."""
    description = db.Column(db.String)
    """description (db.String): Description of this application, possibly including release notes."""
    version = db.Column(db.String)
    """version (db.String): Application version."""
    itunes_store_id = db.Column(db.Integer)
    """itunes_store_id (db.Integer): The application’s iTunes Store ID."""
    bundle_id = db.Column(db.String, index=True, nullable=False)
    """bundle_id (db.String): The application bundle identifier."""
    purchase_method = db.Column(db.Enum(PurchaseMethod))
    """purchase_method (db.Integer): Used in the Options key of InstallApplication to denote the purchase method."""
    manifest_url = db.Column(db.String)
    """manifest_url (db.String): The application manifest URL if iTunesStoreID is not supplied (an enterprise app)."""
    management_flags = db.Column(db.Integer)
    """management_flags (ManagementFlag): Denotes whether app is removed with MDM profile, and whether the user may back
        up application data."""
    change_management_state = db.Column(db.String, default="Managed")
    """change_management_state (db.String): Take ownership of an existing application that is unmanaged."""
    discriminator = db.Column(db.String(20))
    """discriminator (str): The type of application"""

    # iTunes Search API - Cached Result
    country = db.Column(db.String(2))
    """country (str): The two letter country code of the store country. We cache this to avoid assigning apps to devices
        that cannot even install them due to the Apple ID residing in a different locale."""

    artist_id = db.Column(db.Integer)
    """artist_id (int): The iTunes Artist ID, which is commonly the developer in the app store."""
    artist_name = db.Column(db.String)
    """artist_id (str): The iTunes Artist Name, which is commonly the developer in the app store."""
    artist_view_url = db.Column(db.String)
    artwork_url60 = db.Column(db.String)
    """artwork_url60 (str): A URL to the 60x60 icon for this result."""
    artwork_url100 = db.Column(db.String)
    """artwork_url100 (str): A URL to the 100x100 icon for this result."""
    artwork_url512 = db.Column(db.String)
    """artwork_url512 (str): A URL to the 512x512 icon for this result."""
    release_notes = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    minimum_os_version = db.Column(db.String)
    file_size_bytes = db.Column(db.BigInteger)

    tags = db.relationship(
        'Tag',
        secondary=application_tags,
        backref='applications'
    )

    __mapper_args__ = {
        'polymorphic_on': discriminator,
        'polymorphic_identity': 'applications',
    }


class EnterpriseMacApplication(Application):
    """Polymorphic single table inheritance specifically for Enterprise Mac Applications.

    These applications are .pkg files which are often distributed by the MDM or from a host outside of the App Store.
    """
    __mapper_args__ = {
        'polymorphic_identity': ApplicationType.ENTERPRISE_MAC.value
    }


class EnterpriseiOSApplication(Application):
    """Polymorphic single table inheritance specifically for Enterprise iOS Applications.

    These applications are .ipa files which are often distributed by the MDM or from a host outside of the App Store.
    With or without provisioning profiles.
    """
    __mapper_args__ = {
        'polymorphic_identity': ApplicationType.ENTERPRISE_IOS.value
    }


class AppstoreMacApplication(Application):
    """Polymorphic single table inheritance specifically for MAS (App Store) Mac Applications.

    These applications are distributed by VPP using an iTunes Store ID
    """
    __mapper_args__ = {
        'polymorphic_identity': ApplicationType.APPSTORE_MAC.value
    }


class AppstoreiOSApplication(Application):
    """Polymorphic single table inheritance specifically for App Store iOS Applications.

    These applications are distributed by VPP using an iTunes Store ID
    """
    __mapper_args__ = {
        'polymorphic_identity': ApplicationType.APPSTORE_IOS.value
    }


class ApplicationManifest(db.Model):
    """An application manifest describes a non-App store installable application.

    See: `macOS Application <https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/MobileDeviceManagementProtocolRef/3-MDM_Protocol/MDM_Protocol.html#//apple_ref/doc/uid/TP40017387-CH3-SW755>`_.

    :table: application_manifests
    """
    __tablename__ = 'application_manifests'

    id = db.Column(db.Integer, primary_key=True)
    """id (db.Integer): ID"""
    bundle_id = db.Column(db.String, index=True, nullable=False)
    """bundle_id (db.String): Bundle Identifier of the top-level distribution package."""
    bundle_version = db.Column(db.String, index=True)
    """bundle_version (db.String): Bundle Version of the top-level distribution package."""
    kind = db.Column(db.String, default='software')
    """kind (db.String): Type of item to install, at the moment ignored and always set to 'software'."""
    size_in_bytes = db.Column(db.BigInteger)
    """size_in_bytes (db.BigInteger): Size of the package (in bytes)."""
    subtitle = db.Column(db.String)
    """subtitle (db.String):"""
    title = db.Column(db.String)
    """title (db.String):"""
    full_size_image_url = db.Column(db.String)
    """full_size_image_url (db.String): URL to full size image. may be null"""
    full_size_image_needs_shine = db.Column(db.Boolean, default=False)
    """full_size_image_needs_shine (db.Boolean): Whether the image needs the shine effect placed over it."""
    display_image_url = db.Column(db.String)
    """display_image_url (db.String): URL to display image. may be null"""
    display_image_needs_shine = db.Column(db.Boolean, default=False)
    """display_image_needs_shine (db.Boolean): Whether the display image needs the shine effect placed over it."""
    checksums = db.relationship('ApplicationManifestChecksum', back_populates='application_manifest')


class ApplicationManifestChecksum(db.Model):
    __tablename__ = 'application_manifest_checksums'

    id = db.Column(db.Integer, primary_key=True)
    """id (db.Integer): ID"""
    application_manifest_id = db.Column(db.Integer, db.ForeignKey('application_manifests.id'))
    """application_manifest_id (db.Integer): Foreign key reference to the parent manifest."""
    application_manifest = db.relationship(ApplicationManifest, back_populates='checksums')
    """application_manifest (db.relationship): Relationship to the parent manifest."""
    checksum_index = db.Column(db.Integer, nullable=False)
    """checksum_index (db.Integer): Index of this checksum in the sequence of checksums."""
    checksum_value = db.Column(db.String(32), nullable=False)
    """checksum_value (db.String): 32 byte MD5 checksum of this chunk. Chunk size is defined as 10485760 bytes (10mb)"""


class AppSourceType(Enum):
    S3 = 'S3'
    Munki = 'Munki'


class ApplicationSource(db.Model):
    """This table holds rows indicating sources that may referenced in ``InstallApplication`` commands.

    The MDM may require write access to create application manifests from existing items.

    :table: application_sources
    """
    __tablename__ = 'application_sources'

    id = db.Column(db.Integer, primary_key=True)
    """id (db.Integer): ID"""
    name = db.Column(db.String)
    """name (db.String): A short, descriptive name for the source. Only used in display."""
    source_type = db.Column(db.Enum(AppSourceType), default=AppSourceType.Munki)
    """source_type (AppSourceType): The application source type."""

    endpoint = db.Column(db.String)
    """endpoint (db.String): The hostname for object storage or URI for read-only munki repositories."""
    mount_uri = db.Column(db.String)
    """mount_uri (db.String): The R/W mount URI for munki repositories only."""
    use_ssl = db.Column(db.Boolean)
    """use_ssl (Boolean): Use SSL when connecting to endpoint. Used when endpoint is host only."""

    # For S3 / Minio
    access_key = db.Column(db.String)
    """access_key (db.String): The access key for S3 / Minio that uniquely identifies this client."""
    secret_key = db.Column(db.String)
    """secret_key (db.String): The secret key for S3 / Minio that authenticates this client."""
    bucket = db.Column(db.String)
    """bucket (db.String): The bucket name that holds installation packages."""

