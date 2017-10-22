from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4
from enum import Enum, IntFlag

from ..models import db
from ..mutablelist import MutableList


class ManagementFlag(IntFlag):
    NOTHING = 0
    REMOVE_APP_WITH_ENROLLMENT = 1
    PREVENT_APPDATA_BACKUP = 4


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    version = db.Column(db.String)
    itunes_store_id = db.Column(db.Integer)
    bundle_id = db.Column(db.String, index=True, nullable=False)
    purchase_method = db.Column(db.Integer)
    manifest_url = db.Column(db.String)
    management_flags = db.Column(db.Integer)
    change_management_state = db.Column(db.String)


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

