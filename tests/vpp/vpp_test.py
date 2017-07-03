import pytest
import json
import base64
from commandment.vpp.vpp import VPP, encode_stoken

SIMULATOR_STOKEN = {
    'token': 'VGhpcyBpcyBhIHNhbXBsZSB0ZXh0IHdoaWNoIHdhcyB1c2VkIHRvIGNyZWF0ZSB0aGUgc2ltdWxhdG9yIHRva2VuCg==',
    'expDate': '2018-07-03T13:48:31+10:00',
    'orgName': 'Example Inc.'
}

# expect:
# {"token":"VGhpcyBpcyBhIHNhbXBsZSB0ZXh0IHdoaWNoIHdhcyB1c2VkIHRvIGNyZWF0ZSB0aGUgc2ltdWxhdG9yIHRva2VuCg==","expDate":"2018-07-03T13:48:31+10:00","orgName":"Example Inc."}
# {"token": "VGhpcyBpcyBhIHNhbXBsZSB0ZXh0IHdoaWNoIHdhcyB1c2VkIHRvIGNyZWF0ZSB0aGUgc2ltdWxhdG9yIHRva2VuCg==", "expDate": "2018-07-03T13:48:31+10:00", "orgName": "Example Inc."}

SERVICE_CONFIG = {
    "associateLicenseSrvUrl": "http://localhost:8080/associateVPPLicenseSrv",
    "clientConfigSrvUrl": "http://localhost:8080/VPPClientConfigSrv",
    "contentMetadataLookupUrl": "https://uclient-api.itunes.apple.com/WebObjects/MZStorePlatform.woa/wa/lookup",
    "disassociateLicenseSrvUrl": "http://localhost:8080/disassociateVPPLicenseSrv",
    "editUserSrvUrl": "http://localhost:8080/editVPPUserSrv",
    "getLicensesSrvUrl": "http://localhost:8080/getVPPLicensesSrv",
    "getUserSrvUrl": "http://localhost:8080/getVPPUserSrv",
    "getUsersSrvUrl": "http://localhost:8080/getVPPUsersSrv",
    "getVPPAssetsSrvUrl": "http://localhost:8080/getVPPAssetsSrv",
    "invitationEmailUrl": "http://buy.itunes.apple.com/us/vpp-associate?inviteCode=%25inviteCode%25\u0026mt=8",
    "manageVPPLicensesByAdamIdSrvUrl": "http://localhost:8080/manageVPPLicensesByAdamIdSrv",
    "maxBatchAssociateLicenseCount": 10,
    "maxBatchDisassociateLicenseCount": 10,
    "registerUserSrvUrl": "http://localhost:8080/registerVPPUserSrv",
    "retireUserSrvUrl": "http://localhost:8080/retireVPPUserSrv",
    "status": 0,
    "vppWebsiteUrl": "https://vpp.itunes.apple.com/"
}

VPP_MOCK_USER_CID = 'F33D9E0F-CDE3-427E-A444-B137BEF9EFA2'
VPP_MOCK_USER_ID = 2878111686099947
VPP_MOCK_USER_EMAIL = 'vpp-test@localhost'


@pytest.fixture()
def vpp() -> VPP:
    return VPP(
        stoken=encode_stoken(SIMULATOR_STOKEN).decode('utf8'),
        vpp_service_config_url='http://localhost:8080/VPPServiceConfigSrv',
        service_config=SERVICE_CONFIG
    )


class TestVPP:

    # def test_vpp_init(self, vpp):
    #     assert vpp is not None

    def test_vpp_register_user(self, vpp: VPP):
        reply = vpp.register_user(VPP_MOCK_USER_CID, VPP_MOCK_USER_EMAIL)
        assert reply['status'] == 0
        assert 'user' in reply

    def test_getuser_by_client_id(self, vpp: VPP):
        reply = vpp.get_user(client_user_id=VPP_MOCK_USER_CID)
        assert reply['status'] == 0
        assert 'user' in reply

    # def test_getuser_by_client_id_with_itshash(self, vpp):
    #     reply = vpp.get_user(client_user_id=VPP_MOCK_USER_ID, its_id_hash='')

    def test_getuser_by_user_id(self, vpp: VPP):
        reply = vpp.get_user(user_id=VPP_MOCK_USER_ID)
        assert reply['status'] == 0
        assert 'user' in reply

    def test_retireuser_by_client_id(self, vpp: VPP):
        reply = vpp.retire_user(client_user_id=VPP_MOCK_USER_CID)
        assert reply['status'] == 0

    def test_already_retired_by_client_id(self, vpp: VPP):
        reply = vpp.retire_user(client_user_id=VPP_MOCK_USER_CID)
        assert reply['status'] == 0

    # def test_retireuser_by_user_id(self, vpp: VPP):
    #     reply = vpp.retire_user(client_user_id=VPP_MOCK_USER_CID)
    #     assert reply['status'] == 0

    
