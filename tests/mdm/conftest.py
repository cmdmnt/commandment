import pytest
import os
from tests.conftest import *
from commandment.models import Device
from sqlalchemy.orm.session import Session

TEST_DIR = os.path.realpath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.realpath(TEST_DIR + '/../../testdata')


@pytest.fixture(scope='function')
def device(session: Session):
    """Create a fixture device which is referenced in all of the fake MDM responses by its UDID."""
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
    with open(os.path.join(TEST_DATA_DIR, 'AvailableOSUpdates/10.12.5.xml'), 'r') as fd:
        plist_data = fd.read()

    return plist_data
