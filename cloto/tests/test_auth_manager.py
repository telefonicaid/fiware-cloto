__author__ = 'gjp'
from django.test import TestCase
from cloto.models import *
from cloto.manager import AuthorizationManager
from mockito import *
from keystoneclient.v2_0 import client
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized


class AuthorizationManagerTests(TestCase):
    def setUp(self):
        self.token = "ff01eb8a8d69418c95f0009dda9bc1852"
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://130.206.80.61:35357/v2.0"
        self.a = AuthorizationManager.AuthorizationManager()
        self.mockedClient = client
        self.auth = mock()
        self.auth.__setattr__("auth_token", self.authToken)
        when(self.mockedClient).Client(username="admin", password="openstack", auth_url=self.url).thenReturn(self.auth);
        when(self.mockedClient).Client(username="admin", password="fake", auth_url=self.url).thenRaise(Unauthorized());
        self.a.myClient = self.mockedClient

    def test_generate_adminToken(self):
        result = self.a.generate_adminToken("admin", "openstack", self.url)
        self.assertEqual(result, self.authToken)

    def test_generate_adminToken_exception(self):
        try:
            self.a.generate_adminToken("admin", "openstack2", self.url)
        except Unauthorized as ex:
            self.assertRaises(ex)
