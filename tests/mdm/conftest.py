import pytest
import os
from commandment.models import db as _db, Device
from sqlalchemy.orm import scoped_session

TEST_DIR = os.path.realpath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.realpath(TEST_DIR + '/../../testdata')


@pytest.fixture(scope='function')
def device(session: scoped_session):
    d = Device(
        udid='00000000-1111-2222-3333-444455556666',
        device_name='commandment-mdmclient'
    )
    session.add(d)
    session.commit()


@pytest.fixture()
def authenticate_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'Authenticate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'TokenUpdate/10.12.2.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def tokenupdate_user_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'TokenUpdate/10.12.2-user.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def checkout_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'CheckOut/10.11.x.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data


@pytest.fixture()
def available_os_updates_request() -> str:
    with open(os.path.join(TEST_DATA_DIR, 'AvailableOSUpdates'), 'r') as fd:
        plist_data = fd.read()

    return plist_data
