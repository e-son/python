import unittest
import eson


class TestDatetime(unittest.TestCase):

    def setUp(self):
        self.stable_data = ('['
            '#core/datetime "1500-01-20T04:47:47", '
            '#core/datetime "1600-02-19T08:47:47.123456", '
            '#core/datetime "1700-03-18T12:47:47+08:30", '
            '#core/datetime "1800-04-17T16:47:47.123456-01:30", '
            '#core/datetime "1900-05-16T20:47:47-00:30"'
        ']')
        self.unstable_data = ('['
            '#core/datetime "1500-01-20T04:47:47Z", '
            '#core/datetime "1600-02-19T08:47:47.123+00:30", '
            '#core/datetime "1700-03-18T12:47:47.0Z", '
            '#core/datetime "1800-04-17T16:47:47.123456789-00:30"'
        ']')

    def test_stable_data(self):
        """ #core/datetime should be encoded and decoded properly"""
        obj1 = eson.loads(self.stable_data)
        str1 = eson.dumps(obj1)
        obj2 = eson.loads(str1)
        self.assertEqual(self.stable_data, str1)
        self.assertEqual(obj1, obj2)

    def test_unstable_data(self):
        """ #core/datetime should be encoded and decoded properly"""
        obj1 = eson.loads(self.unstable_data)
        str1 = eson.dumps(obj1)
        obj2 = eson.loads(str1)
        str2 = eson.dumps(obj2)
        self.assertEqual(str1, str2)
        self.assertEqual(obj1, obj2)

