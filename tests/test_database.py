"""test_database.py: Tests for the database linkage [partial]"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

from commandment import database
import datetime

from fixtures import app

class TestJSONEncodedDict:
    def test_process_bind_param_accepts_none_value(self):
        json_encoded_dict = database.JSONEncodedDict()
        assert json_encoded_dict.process_bind_param(None, []) is None

    def test_process_bind_param_accepts_string_dict(self):
        json_encoded_dict = database.JSONEncodedDict()
        testdict = {
            'testing': 'this'
        }
        json_string = '{"testing":"this"}'
        assert json_encoded_dict.process_bind_param(testdict, []) == json_string

    def test_process_bind_param_accepts_datetime_in_dict(self):
        json_encoded_dict = database.JSONEncodedDict()
        testdict = {
            'testing': datetime.datetime(2014, 10, 1, 13, 59, 12)
        }
        json_string = '{"testing":"2014-10-01 13:59:12"}'
        assert json_encoded_dict.process_bind_param(testdict, []) == json_string
