import pytest
import requests
from commandment.dep.dep import DEP

SIMULATOR_URL = 'http://localhost:8080'


@pytest.fixture
def simulator_token() -> dict:
    res = requests.get('{}/token'.format(SIMULATOR_URL))
    return res.json()


@pytest.fixture
def dep(simulator_token: dict) -> DEP:
    d = DEP(
        consumer_key=simulator_token['consumer_key'],
        consumer_secret=simulator_token['consumer_secret'],
        access_token=simulator_token['access_token'],
        access_secret=simulator_token['access_secret'],
    )

    return d
