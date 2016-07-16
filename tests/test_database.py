"""test_database.py: Tests for the database linkage [partial]"""

__author__ = "Phil Weir <phil.weir@flaxandteal.co.uk>"

from commandment import database
import datetime

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
