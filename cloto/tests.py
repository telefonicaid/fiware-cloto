__author__ = 'Geon'
from django.test import TestCase
from django.test.client import RequestFactory
from cloto.restCloto import GeneralView


class GeneralTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_api_info(self):
        # Create an instance of a GET request.
        request = self.factory.get('/v1.0/tenantId/')

        # Test my_view() as if it were deployed at /customer/details
        response = GeneralView().GET(request, "tenantId")
        self.assertEqual(response.status_code, 200)

    def test_update_window(self):
        # Create an instance of a GET request.
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": 4}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = GeneralView().PUT(request, "tenantId")
        self.assertEqual(response.status_code, 200)

    def test_not_update_window(self):
        # Create an instance of a GET request.
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": pepe}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = GeneralView().PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)
