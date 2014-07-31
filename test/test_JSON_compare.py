import unittest
import eson
import json
from test.helpers.JSONs import generate


class TestEncoder(unittest.TestCase):
    pass


class TestDecoder(unittest.TestCase):
    pass


for name, data in generate():

    def test_encode(self):
        """ eson should encode json object like a json"""
        str1 = json.dumps(data)
        str2 = eson.dumps(data)
        self.assertEqual(str1, str2, "eson and json differ encoding %s" % name)

    setattr(TestEncoder, "test_%s" % name, test_encode)

    def test_decode(self):
        """ eson should decode json object like a json"""
        str0 = json.dumps(data)
        data1 = json.loads(str0)
        data2 = eson.loads(str0)
        self.assertEqual(data1, data2, "eson and json differ decoding %s" % name)

    setattr(TestDecoder, "test_%s" % name, test_decode)



