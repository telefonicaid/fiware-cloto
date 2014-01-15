__author__ = 'gjp'
from django.test import TestCase, Client
from cloto.manager import AuthorizationManager
from mockito import *
from keystoneclient.v2_0 import client, tokens


class ClientTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://130.206.80.61:35357/v2.0"
        self.mockedClient = client
        self.auth = mock()
        self.auth.stub("authenticate")
        self.auth.__setattr__("auth_token", self.authToken)
        when(self.auth.stub("tokens")).authenticate(token="1234").thenReturn(True);
        when(AuthorizationManager.AuthorizationManager)\
            .checkToken(self.authToken, "1234", "tenantId", self.url).thenReturn(True);
        when(AuthorizationManager.AuthorizationManager).\
            generate_adminToken("admin", "openstack", self.url).thenReturn(self.authToken);

    def test_servers_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/', **{'HTTP_X_AUTH_TOKEN': '1234'})

    def test_server_rules_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/rules', **{'HTTP_X_AUTH_TOKEN': '1234'})
