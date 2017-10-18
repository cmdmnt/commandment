from ..dbtypes import GUID, JSONEncodedDict
from uuid import uuid4

from ..models import db


class ApplicationManifest(db.Model):
    __tablename__ = 'applications_manifests'

    id = db.Column(db.Integer, primary_key=True)
    bundle_id = db.Column(db.String, index=True, nullable=False)
    bundle_version = db.Column(db.String, index=True)
    kind = db.Column(db.String, default='software')
    size_in_bytes = db.Column(db.BigInteger)
    subtitle = db.Column(db.String)
    title = db.Column(db.String)


class ApplicationManifestChecksum(db.Model):
    __tablename__ = 'application_manifest_checksums'

    id = db.Column(db.Integer, primary_key=True)
    application_manifest_id = db.Column(db.Integer, db.ForeignKey('application_manifests.id'))
    application_manifest = db.relationship(ApplicationManifest, back_populates='checksums')
    checksum_index = db.Column(db.Integer, nullable=False)
    checksum_value = db.Column(db.String, nullable=False)

