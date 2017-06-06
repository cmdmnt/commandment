from marshmallow import Schema, fields


class Asset(Schema):
    kind = fields.String(default='software-package')
    md5_size = fields.Integer(default=10485760)
    md5s = fields.List(fields.String())
    url = fields.URL()
    needs_shine = fields.Boolean()
    

class BundleItem(Schema):
    bundle_identifier = fields.String()
    bundle_version = fields.String()


class Metadata(Schema):
    bundle_identifier = fields.String()
    bundle_version = fields.String()
    items = fields.Nested(BundleItem, many=True)
    kind = fields.String()
    sizeInBytes = fields.String()
    subtitle = fields.String()
    title = fields.String()


class ManifestItem(Schema):
    assets = fields.Nested(Asset, many=True)
    metadata = fields.Nested(Metadata)


class Manifest(Schema):
    items = fields.Nested(ManifestItem, many=True)

