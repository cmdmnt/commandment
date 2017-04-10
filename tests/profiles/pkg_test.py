import pytest
from commandment.profiles import Payload, PAYLOADS

class TestPayloads:

    def test_payloads_metaclass(self):
        p = Payload('test', 'org.example.identifier')
        print(PAYLOADS)
