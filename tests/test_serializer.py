"""test_encoder.py: Tests enhanced JSON serialization"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

from commandment import serializer
import datetime
import pytest
import json

from fixtures import app

class TestJSONMobileEncoder:
    def test_cannot_serialize_unknown_type(self):
        encoder = serializer.JSONMobileEncoder()
        obj = object()
        assert obj == encoder.default(obj)

    def test_can_serialize_datetime(self):
        encoder = serializer.JSONMobileEncoder()
        test_date = datetime.datetime(2000, 1, 1, 12, 10, 10)
        assert encoder.default(test_date) == '2000-01-01 12:10:10'

    def test_can_dump_datetime(self):
        test_dict = {'abc': datetime.datetime(2000, 1, 1, 12, 10, 10)}
        assert json.dumps(test_dict, cls=serializer.JSONMobileEncoder)
