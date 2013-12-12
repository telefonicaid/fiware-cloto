__author__ = 'gjp'
from django.test import TestCase
import cloto.information as information
import datetime


class InformationTests(TestCase):
    def setUp(self):
        self.body1 = "{\"windowsize\": 4}"
        self.expect1 = 4
        self.body2 = "{\"windowsize\": notValidWindowSize}"
        self.info = information.information("test", "test", "test", datetime.datetime.now(), "test")

    def test_parseInfo(self):
        info = self.info.parse(self.body1)
        self.assertEqual(info.windowsize, self.expect1)

    def test_parseInfo_Error(self):
        info = self.info.parse(self.body2)
        self.assertEqual(info, None)

    def test_get_vars(self):
        result = self.info.getVars()
        self.assertEqual(result, vars(self.info))
