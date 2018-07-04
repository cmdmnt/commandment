from ..dbtypes import GUID, JSONEncodedDict
from .enum import VPPUserStatus, VPPPricingParam, VPPProductType

from ..models import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import base64
import json
import dateutil.parser


class VPPAccount(db.Model):
    __tablename__ = 'vpp_accounts'

    id = db.Column(db.Integer, primary_key=True)

    @hybrid_property
    def stoken(self) -> str:
        return self._stoken

    @stoken.setter
    def stoken(self, value: str):
        self._stoken = value
        decoded = base64.b64decode(value)
        data = json.loads(decoded)
        self.exp_date = dateutil.parser.parse(data['expDate'])
        self.org_name = data['orgName']

    _stoken = db.Column(db.String, nullable=False)
    exp_date = db.Column(db.DateTime)
    """datetime: Populated for convenience when checking the VPP token expiry date."""
    org_name = db.Column(db.String)
    """string: Populated for convenience."""

    # at least one of these must be null at all times
    licenses_since_modified_token = db.Column(db.String)
    licenses_batch_token = db.Column(db.String)

    users_since_modified_token = db.Column(db.String)
    users_batch_token = db.Column(db.String)

    # ASM/ABM Location Information
    location_id = db.Column(db.Integer)
    location_name = db.Column(db.String)


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
    

