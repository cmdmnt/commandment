from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4
from enum import Enum, IntEnum, IntFlag

from ..models import db
from ..mutablelist import MutableList


class ManagementFlag(IntFlag):
    NOTHING = 0
    REMOVE_APP_WITH_ENROLLMENT = 1
    PREVENT_APPDATA_BACKUP = 4


class PurchaseMethod(IntEnum):
    LEGACY_VPP = 0
    VPP_APP_ASSIGNMENT = 1


class ApplicationType(Enum):
    """A list of the polymorphic identities available for subclasses of Application."""
    ENTERPRISE_MAC = 'enterprise_mac'
    ENTERPRISE_IOS = 'enterprise_ios'
    APPSTORE_MAC = 'appstore_mac'
    APPSTORE_IOS = 'appstore_ios'


class Application(db.Model):
    """This table holds details of each individual application (either app store or enterprise application).

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
    purchase_method = db.Column(db.Integer)
    """purchase_method (db.Integer): Used in the Options key of InstallApplication to denote the purchase method."""
    manifest_url = db.Column(db.String)
    """manifest_url (db.String): The application manifest URL if iTunesStoreID is not supplied (an enterprise app)."""
    management_flags = db.Column(db.Integer)
    """management_flags (ManagementFlag): Denotes whether app is removed with MDM profile, and whether the user may back
        up application data."""
    change_management_state = db.Column(db.String)
    """change_management_state (db.String): Take ownership of an existing application that is unmanaged."""
    discriminator = db.Column(db.String(20))
    """discriminator (str): The type of application"""

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
        'polymorphic_identity': ApplicationType.APPSTORE_MAC.value
    }


class ApplicationManifest(db.Model):
    __tablename__ = 'applications_manifests'

    id = db.Column(db.Integer, primary_key=True)
    bundle_id = db.Column(db.String, index=True, nullable=False)
    bundle_version = db.Column(db.String, index=True)
    kind = db.Column(db.String, default='software')
    size_in_bytes = db.Column(db.BigInteger)
    subtitle = db.Column(db.String)
    title = db.Column(db.String)
    checksums = db.relationship('ApplicationManifestChecksum', back_populates='application_manifest')


class ApplicationManifestChecksum(db.Model):
    __tablename__ = 'application_manifest_checksums'

    id = db.Column(db.Integer, primary_key=True)
    application_manifest_id = db.Column(db.Integer, db.ForeignKey('applications_manifests.id'))
    application_manifest = db.relationship(ApplicationManifest, back_populates='checksums')
    checksum_index = db.Column(db.Integer, nullable=False)
    checksum_value = db.Column(db.String, nullable=False)


class App(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String, nullable=False, unique=True)
    filesize = db.Column(db.Integer, nullable=False)

    md5_hash = db.Column(db.String(32), nullable=False)  # MD5 hash of the entire file

    # MDM clients support a chunked method of retrival of the download file
    # presumably to best support OTA download of large updates. These fields
    # are in support of that mechanism
    md5_chunk_size = db.Column(db.Integer, nullable=False)
    md5_chunk_hashes = db.Column(db.Text, nullable=True)  # colon (:) separated list of MD5 chunk hashes

    bundle_ids_json = db.Column(MutableList.as_mutable(JSONEncodedDict), nullable=True)
    pkg_ids_json = db.Column(MutableList.as_mutable(JSONEncodedDict), nullable=True)

    def path_format(self):
        return '%010d.dat' % self.id

    def __repr__(self):
        return '<App ID=%r Filename=%r>' % (self.id, self.filename)


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

