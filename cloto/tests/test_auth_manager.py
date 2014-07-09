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
        self.fakeToken = "fffffffffffffffffffffffffffffffff"
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://130.206.80.61:35357/v2.0"
        self.tenantId = "6571e3422ad84f7d828ce2f30373b3d4"
        self.a = AuthorizationManager.AuthorizationManager()
        self.mockedClient = client
        self.auth = mock()
        self.tokenM = mock()

        self.auth.__setattr__("auth_token", self.authToken)
        self.auth.__setattr__("tokens", self.tokenM)
        when(self.tokenM).authenticate(token=self.token, tenant_id=self.tenantId).thenReturn("Is valid")
        when(self.mockedClient).Client(username="admin", password="realpass", auth_url=self.url).thenReturn(self.auth)
        when(self.mockedClient).Client(token=self.authToken, auth_url=self.url).thenReturn(self.auth)
        when(self.mockedClient).Client(username="admin", password="fake", auth_url=self.url).thenRaise(Unauthorized())
        self.a.myClient = self.mockedClient

    def test_generate_adminToken(self):
        result = self.a.generate_adminToken("admin", "realpassword", self.url)
        self.assertEqual(result, self.authToken)

    def test_generate_adminToken_exception(self):
        try:
            self.a.generate_adminToken("admin", "fake", self.url)
        except Unauthorized as ex:
            self.assertRaises(ex)

#    def test_check_token(self):
#        result = self.a.checkToken(self.authToken, self.token, self.tenantId, self.url)
#        self.assertEqual(result, self.authToken)

#    def test_check_token_exception(self):
#       try:
#           result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId, self.url)
#      except Unauthorized as ex:
#          self.assertRaises(ex)
