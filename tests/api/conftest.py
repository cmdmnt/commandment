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
