import pytest
import logging

from commandment.vpp.enum import LicenseAssociationType
from commandment.vpp.vpp import VPP

logger = logging.getLogger(__name__)

VPP_MOCK_USER_CID = 'F33D9E0F-CDE3-427E-A444-B137BEF9EFA2'
VPP_MOCK_USER_ID = 2878111686099947
VPP_MOCK_USER_EMAIL = 'vpp-test@localhost'
VPP_MOCK_USER_EMAIL_2 = 'vpp-test-2@localhost'
VPP_BATCH_LICENSE_ADAMID = 525463029  # This license is used as the test for large batch operations


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

    # def test_already_retired_by_client_id(self, vpp: VPP):
    #     reply = vpp.retire_user(client_user_id=VPP_MOCK_USER_CID)
    #     assert reply['status'] == 0

    # def test_retireuser_by_user_id(self, vpp: VPP):
    #     reply = vpp.retire_user(client_user_id=VPP_MOCK_USER_CID)
    #     assert reply['status'] == 0

    def test_edit_user_by_client_id(self, vpp: VPP):
        reply = vpp.edit_user(client_user_id=VPP_MOCK_USER_CID, email=VPP_MOCK_USER_EMAIL_2)
        assert reply['status'] == 0
        assert reply['user']['email'] == VPP_MOCK_USER_EMAIL_2

    def test_get_assets(self, vpp: VPP):
        reply = vpp.assets()
        assert 'assets' in reply

    # def test_get_licenses(self, vpp: VPP):
    #     licenses = vpp.licenses()
    #     print(licenses)

    def test_users(self, vpp: VPP):
        cursor = vpp.users()
        while cursor.next():
            users = cursor.users
            print(users)

        print('cursor exhausted')

    def test_licenses(self, vpp: VPP):
        cursor = vpp.licenses(VPP_BATCH_LICENSE_ADAMID)
        licenses = []
        total = cursor.total
        assert len(cursor.licenses) == 600
        licenses = licenses + cursor.licenses

        while cursor.next():
            licenses = licenses + cursor.licenses

        assert len(licenses) == total

    def test_manage_one_license(self, vpp: VPP):
        op = vpp.manage(VPP_BATCH_LICENSE_ADAMID)

        op.add(LicenseAssociationType.ClientUserID, VPP_MOCK_USER_CID)
        vpp.save(op)
        