from typing import List
from functools import partial
from uuid import UUID
from enum import Enum


class PayloadScope(Enum):
    User = 'User'
    System = 'System'

def profile(identifier: str, type: str, payloads: List[dict], scope: PayloadScope) -> dict:

    p = {
        'PayloadType': type,
        'PayloadUUID': UUID(),
        'PayloadVersion': 1,
        'PayloadIdentifier': 'dev.commandment.profile-service',
        'PayloadDisplayName': 'Commandment Profile Service',
        'PayloadContent': payloads
    }

    return p

profile_factory = partial(profile, 'dev.comandment.profile-service')