import pytest
import requests

SIMULATOR_URL = 'http://localhost:8080'


@pytest.fixture
def simulator_token() -> str:
    res = requests.get('{}/internal/get_stoken'.format(SIMULATOR_URL))
    return res.json().get('sToken', None)

