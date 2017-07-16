import pytest
import requests
from commandment.dep.dep import DEP

SIMULATOR_URL = 'http://localhost:8080'


@pytest.fixture
def simulator_token() -> dict:
    res = requests.get('{}/token'.format(SIMULATOR_URL))
    return res.json()

