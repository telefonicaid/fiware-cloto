from nose.tools import assert_equal

__author__ = 'Geon'
from django.test import TestCase
import datetime
import cloto.information as information
from django.test.client import RequestFactory
from mockito import *

from cloto.restCloto import GeneralView


class GeneralTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        myMock = mock()
        mockedInfo = information.information(None, "test", "test", "test", datetime.datetime.now(), "test")
        validWindowSize = "4"
        validWindowSizeValue = 5
        invalidWindowSize = "notValidValue"
        # when(myMock).startingParameters("tenantId").thenReturn(mockedInfo)
        # when(myMock).getVars(myMock).thenReturn(vars(mockedInfo))
        when(myMock).updateWindowSize("tenantId", validWindowSizeValue).thenReturn(mockedInfo)
        when(myMock).updateWindowSize("tenantId", invalidWindowSize).thenReturn(None)

        when(myMock).parse("{\"windowsize\": %s}" % validWindowSize).thenReturn(mockedInfo)
        when(myMock).parse("{\"windowsize\": %s}" % invalidWindowSize).thenReturn(None)
        self.general = GeneralView()
        self.general.set_info(myMock)

    def test_get_api_info(self):
        # Create an instance of a GET request.
        request = self.factory.get('/v1.0/tenantId/')

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.GET(request, "tenantId")
        self.assertEqual(response.status_code, 200)

    def test_update_window(self):
        # Create an instance of a GET request.
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": 4}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 200)

    def test_not_update_window(self):
        # Create an instance of a GET request.
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": notValidValue}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)
