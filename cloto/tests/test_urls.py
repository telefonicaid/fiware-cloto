__author__ = 'gjp'
from django.test import TestCase, Client


class ClientTests(TestCase):

    def setUp(self):
        self.c = Client()

    def test_servers_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/')

    def test_server_rules_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/rules')
