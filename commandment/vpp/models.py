from ..dbtypes import GUID, JSONEncodedDict
from .enum import VPPUserStatus, VPPPricingParam, VPPProductType

from ..models import db


class VPPState(db.Model):
    __tablename__ = 'vpp_state'

    id = db.Column(db.Integer, primary_key=True)
    stoken = db.Column(db.String, nullable=False)

    # at least one of these must be null at all times
    licenses_since_modified_token = db.Column(db.String)
    licenses_batch_token = db.Column(db.String)

    users_since_modified_token = db.Column(db.String)
    users_batch_token = db.Column(db.String)


class VPPUser(db.Model):
    __tablename__ = 'vpp_users'

    user_id = db.Column(db.Integer, primary_key=True)
    client_user_id = db.Column(GUID, nullable=False)
    email = db.Column(db.String)
    status = db.Column(db.Enum(VPPUserStatus))
    invite_url = db.Column(db.String)
    invite_code = db.Column(db.String)


class VPPLicense(db.Model):
    __tablename__ = 'vpp_licenses'

    license_id = db.Column(db.Integer, primary_key=True)
    adam_id = db.Column(db.String)
    product_type = db.Column(db.Enum(VPPProductType))
    product_type_name = db.Column(db.String)
    pricing_param = db.Column(db.Enum(VPPPricingParam))
    is_irrevocable = db.Column(db.Boolean)
    user_id = db.Column(db.ForeignKey('vpp_users.user_id'))
    client_user_id = db.Column(db.ForeignKey('vpp_users.client_user_id'))
    its_id_hash = db.Column(db.String)
    

