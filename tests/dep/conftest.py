import pytest
import requests
import os.path
from commandment.dep.dep import DEP

SIMULATOR_URL = 'http://localhost:8080'


@pytest.fixture
def simulator_token() -> dict:
    res = requests.get('{}/token'.format(SIMULATOR_URL))
    return res.json()


@pytest.fixture
def live_token() -> str:
    dep_token_path = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata', 'deptoken.json')
    with open(dep_token_path, 'rb') as fd:
        content = fd.read()

    return content.decode('utf8')


@pytest.fixture
def dep(simulator_token: dict) -> DEP:
    d = DEP(
        consumer_key=simulator_token['consumer_key'],
        consumer_secret=simulator_token['consumer_secret'],
        access_token=simulator_token['access_token'],
        access_secret=simulator_token['access_secret'],
        url=SIMULATOR_URL,
    )

    return d


@pytest.fixture
def dep_live(live_token: str):
    return DEP.from_token(live_token)


@pytest.fixture
def dep_profile() -> dict:
    p = {
        'profile_name': 'Fixture Profile',
        'url': 'https://localhost:5433',
        'allow_pairing': True,
        'is_supervised': True,
        'is_multi_user': False,
        'is_mandatory': False,
        'await_device_configured': False,
        'is_mdm_removable': True,
        'support_phone_number': '12345678',
        'auto_advance_setup': False,
        'support_email_address': 'test@localhost',
        'org_magic': 'COMMANDMENT-TEST-FIXTURE',
        'skip_setup_items': [
            'Biometric'
        ],
        'department': 'Commandment Dept',
        'devices': [],
        'language': 'en',
        'region': 'AU'
    }
    return p