import pytest
import requests
from commandment.vpp.vpp import VPP


SIMULATOR_URL = 'http://localhost:8080'

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


@pytest.fixture
def simulator_token() -> str:
    res = requests.get('{}/internal/get_stoken'.format(SIMULATOR_URL))
    return res.json().get('sToken', None)


@pytest.fixture()
def vpp(simulator_token: str) -> VPP:
    return VPP(
        stoken=simulator_token,
        vpp_service_config_url='http://localhost:8080/VPPServiceConfigSrv',
        service_config=SERVICE_CONFIG
    )
