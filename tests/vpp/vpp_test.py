import pytest
import json
import base64
from commandment.vpp.vpp import VPP

SIMULATOR_STOKEN = {
    'token': 'VGhpcyBpcyBhIHNhbXBsZSB0ZXh0IHdoaWNoIHdhcyB1c2VkIHRvIGNyZWF0ZSB0aGUgc2ltdWxhdG9yIHRva2VuCg==',
    'expDate': '',
    'orgName': 'Example Inc.'
}


@pytest.fixture()
def vpp() -> VPP:
    return VPP(
        stoken=base64.b64encode(json.dumps(SIMULATOR_STOKEN).encode('utf8')),
        vpp_service_config_url='http://localhost:8080/VPPServiceConfigSrv')


class TestVPP:

    def test_vpp_init(self, vpp):
        assert vpp is not None

