#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#

__author__ = 'gjp'
from django.test import TestCase
from mockito import mock, when
from mock import MagicMock
from keystoneclient.v2_0 import client
from keystoneclient.exceptions import Unauthorized, InternalServerError, AuthorizationFailure, ConnectionRefused
from keystoneclient.v2_0.tokens import Token
from requests import Response

from fiware_cloto.cloto.manager import AuthorizationManager
from fiware_cloto.cloto.constants import ACCEPT_HEADER, JSON_TYPE, X_AUTH_TOKEN_HEADER, TOKENS_PATH_V2,\
     TOKENS_PATH_V3, X_SUBJECT_TOKEN_HEADER, AUTH_API_V2, AUTH_API_V3, HTTP_RESPONSE_CODE_OK,\
    HTTP_RESPONSE_CODE_UNAUTHORIZED
from django.utils import timezone


class MySession(MagicMock):
    # Mock of a keystone session

    def Session(self, auth, timeout):
        # Mock of the Keystone session generator
        session_mocked = mock()
        if auth.auth_url != "http://hosturl:35357/v2.0" and auth.auth_url != "http://hosturl:35357/v3":
            raise ConnectionRefused("Unable to establish connection to %s", auth.auth_url)
        if auth.password == "realpassword" or auth.password == None:
            authToken = "77d254b3caba4fb29747958138136ffa"
            when(session_mocked).get_token().thenReturn(authToken)
        else:
            raise AuthorizationFailure(u'{"error": {"message": '
                                       u'"Could not find token: f28d546408bb43e0978ac0d91bd4a7a",'
                                       u' "code": 404, "title": "Not Found"}}')

        return session_mocked


class AuthorizationManagerTests(TestCase):
    def setUp(self):
        self.user = "user"
        self.token = "ff01eb8a8d69418c95f0009dda9bc1852"
        self.token_not_expired = "aa01eb8a8d69418c95f0009dda9bc0000"
        self.token_other_tenant = "gg01eb8a8d69418c95f0009dda9bc1852"
        self.token_not_found = "0001eb8a8d69418c95f0009dda9bc1852"
        self.token_not_authorized = "bbbbbbba8d69418c95f0009dda9bc1852"
        self.fakeToken = "fffffffffffffffffffffffffffffffff"
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://hosturl:35357/v2.0"
        self.url_v3 = "http://hosturl:35357/v3"
        self.url_noResponse = "http://127.0.0.1:35357/v2.0"
        self.url_server_error = "http://serverWithErrors.com:35357/v2.0"
        self.tenantId = "6571e3422ad84f7d828ce2f30373b3d4"
        self.a = AuthorizationManager.AuthorizationManager(self.url, AUTH_API_V2)
        self.mockedClient = client
        self.auth = mock()
        self.tokenM = mock()
        self.session_mocked = mock()
        self.session_client = MySession()
        manager = mock()
        self.requestsMock = mock()
        response = Response()
        response.status_code = HTTP_RESPONSE_CODE_OK
        response._content = '''
        {
            "access": {
                "token": {
                    "expires": "2015-07-09T15:16:07Z",
                    "id": {
                        "token": "ff01eb8a8d69418c95f0009dda9bc1852",
                        "tenant": "6571e3422ad84f7d828ce2f30373b3d4",
                        "name": "user@mail.com",
                        "access_token": "4HMIFCQOlswp1hZmPG-BmP6cXQWyqvIYV0WrvoKptV59O4r3_VpIJwwFx-JgJW",
                        "expires": "2014-09-13T07:23:51.000Z"
                    },
                    "tenant": {
                        "description": "Tenant from IDM",
                        "enabled": true,
                        "id": "6571e3422ad84f7d828ce2f30373b3d4",
                        "name": "user"
                    }
                },
                "user": {
                    "username": "user",
                    "roles_links": [],
                    "id": "user",
                    "roles": [{
                        "id": "8db87ccbca3b4d1ba4814c3bb0d63aab",
                        "name": "Member"
                    }],
                    "name": "user"
                }
            }
        }'''

        response_not_expired = Response()
        response_not_expired.status_code = HTTP_RESPONSE_CODE_OK
        response_not_expired._content = '''
        {
            "access": {
                "token": {
                    "expires":"2115-07-09T15:16:07Z",
                    "id": {
                        "token":"aa01eb8a8d69418c95f0009dda9bc0000",
                        "tenant":"6571e3422ad84f7d828ce2f30373b3d4",
                        "name":"user@mail.com",
                        "access_token": "4HMIFCQOlswp1hZmPG-BmP6cXQWyqvIYV0WrvoKptV59O4r3_VpIJwwFx-JgJW",
                        "expires":"2114-09-13T07:23:51.000Z"
                    },
                    "tenant":{
                        "description":"Tenant from IDM","enabled":true,
                        "id":"6571e3422ad84f7d828ce2f30373b3d4",
                        "name":"user"
                    }
                },
                "user": {
                    "username":"user",
                    "roles_links":[],
                    "id":"user",
                    "roles":[{
                        "id":"8db87ccbca3b4d1ba4814c3bb0d63aab",
                        "name":"Member"
                    }],
                    "name":"user"
                }
            }
        }'''

        response_v3 = Response()
        response_v3.status_code = HTTP_RESPONSE_CODE_OK
        response_v3._content = '''
        {
            "token": {
                "methods": ["password"],
                "roles": [{
                    "id": "ff01eb8a8d69418c95f0009dda9bc1852",
                    "name": "owner"
                }],
                "expires_at": "2015-05-26T13:01:49.632762Z",
                "project": {
                    "domain": {
                        "id": "default", "name": "Default"
                    },
                    "id": "6571e3422ad84f7d828ce2f30373b3d4",
                    "name": "user@mail.com"
                },
                "user": {
                    "domain": {
                        "id": "default","name": "Default"
                    },
                    "id": "user",
                    "name": "user@mail.com"
                },
                "audit_ids": ["XREoG4obSW69erG3fVjvjQ"],
                "issued_at": "2016-03-08T10:06:04.653858Z"
            }
        }'''

        response_v3_fail = Response()
        response_v3_fail.status_code = HTTP_RESPONSE_CODE_UNAUTHORIZED
        response_v3_fail._content = '''{"error": {"message": "The request you have made requires authentication.",
                                    "code": 401, "title": "Unauthorized"}}'''

        response2 = Response()
        response2.status_code = HTTP_RESPONSE_CODE_OK
        response2._content = '''
        {
            "access":{
                "token": {
                    "expires":"2115-07-09T15:16:07Z",
                    "id": {
                        "token": "gg01eb8a8d69418c95f0009dda9bc1852",
                        "tenant": "1111e3422ad84f7d828ce2f30373b3d4",
                        "name": "user@mail.com",
                        "access_token": "4HMIFCQOlswp1hZmPG-BmP6cXQWyqvIYV0WrvoKptV59O4r3_VpIJwwFx-JgJW",
                        "expires": "2114-09-13T07:23:51.000Z"
                    },
                    "tenant": {
                        "description": "Different Tenant from IDM",
                        "enabled": true,
                        "id":"1111e3422ad84f7d828ce2f30373b3d4",
                        "name":"user"
                    }
                },
                "user": {
                    "username": "user",
                    "roles_links": [],
                    "id": "user",
                    "roles": [{
                        "id": "8db87ccbca3b4d1ba4814c3bb0d63aab",
                        "name": "Member"
                    }],
                    "name":"user"
                }
            }
        }'''

        response_not_found = Response()
        response_not_found.status_code = HTTP_RESPONSE_CODE_UNAUTHORIZED
        response_not_found._content = 'User token not found'
        response_not_found._content = '{"unauthorized": {"message": {"error": {"message": "Could not find token: '\
                                      + self.token_not_found + '", "code": 404, "title": "Not Found"}}, "code": 401}}'

        response_not_authorized = Response()
        response_not_authorized.status_code = HTTP_RESPONSE_CODE_OK
        response_not_authorized._content = 'Service not authorized'

        dic_valid = {"token": {"id": self.authToken, "tenant": {"enabled": True,
                        "description": "Default tenant", "name": "admin", "id": "6571e3422ad84f7d828ce2f30373b3d4"}}}
        dic_invalid = {"token": {"id": self.authToken, "tenant": {"enabled": True,
                        "description": "Default tenant", "name": "admin", "id": "anotherTenantId"}}}
        verification_expected = Token(manager, dic_valid)
        verification_expected_fail = Token(manager, dic_invalid)
        self.auth.__setattr__("auth_token", self.authToken)
        self.auth.__setattr__("tokens", self.tokenM)
        when(self.session_mocked).get_token().thenReturn(self.authToken)
        when(self.tokenM).authenticate(token=self.token, tenant_id=self.tenantId).thenReturn(verification_expected)
        when(self.tokenM).authenticate(token=self.fakeToken, tenant_id=self.tenantId)\
            .thenReturn(verification_expected_fail)
        when(self.mockedClient).Client(username="admin", password="realpassword", auth_url=self.url)\
            .thenReturn(self.auth)
        when(self.mockedClient).Client(username="admin", password="realpassword", auth_url=self.url_v3)\
            .thenReturn(self.auth)
        when(self.mockedClient).Client(token=self.authToken, endpoint=self.url).thenReturn(self.auth)
        when(self.mockedClient)\
            .Client(token=self.authToken, endpoint=self.url_noResponse).thenRaise(InternalServerError())
        when(self.mockedClient)\
            .Client(token=self.authToken, endpoint=self.url_server_error).thenRaise(Exception())
        when(self.mockedClient).Client(username="admin", password="fake", auth_url=self.url).thenRaise(Unauthorized())
        when(self.mockedClient)\
            .Client(username="admin", password="fake", auth_url=self.url_server_error)\
            .thenRaise(AuthorizationFailure())

        headers = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: self.authToken}
        headers_v3 = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: self.authToken,
                      X_SUBJECT_TOKEN_HEADER: self.token}
        headers_v3_fake = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: self.fakeToken,
                           X_SUBJECT_TOKEN_HEADER: self.token}

        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token, headers=headers)\
            .thenReturn(response)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_not_expired, headers=headers)\
            .thenReturn(response_not_expired)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V3, headers=headers_v3)\
            .thenReturn(response_v3)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V3, headers=headers_v3_fake)\
            .thenReturn(response_v3_fail)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_other_tenant, headers=headers)\
            .thenReturn(response2)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_not_found, headers=headers)\
            .thenReturn(response_not_found)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_not_authorized, headers=headers)\
            .thenReturn(response_not_authorized)
        when(self.requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.fakeToken, headers=headers)\
            .thenRaise(Unauthorized())
        when(self.requestsMock).get(self.url_noResponse + "/" + TOKENS_PATH_V2 + self.fakeToken, headers=headers)\
            .thenRaise(InternalServerError())
        when(self.requestsMock).get(self.url_server_error + "/" + TOKENS_PATH_V2 + self.token, headers=headers)\
            .thenRaise(Exception())
        self.a.client = self.requestsMock
        self.a.myClient = self.mockedClient
        self.a.session = self.session_client

    def test_generate_adminToken(self):
        """ Test if I get a valid authorization token providing valid user and password.
        """

        result = self.a.get_auth_token("admin", "realpassword", "tenantId",
                                         tenant_name="tenantName")

        self.assertEqual(result, self.authToken)

    def test_generate_adminToken_exception(self):
        """ Test if I get an AuthorizationFailure exception while asking for an authorization token
        providing a valid user with fake password.
        """
        try:
            self.a.get_auth_token("admin", "fake", "tenantId", tenant_name="tenantName")
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_generate_adminToken_exception_2(self):
        """ Test if I get a ConnectionRefused exception while asking for an authorization token
        providing valid user and password.
        """
        try:
            self.a.identity_url = self.url_server_error
            self.a.get_auth_token("admin", "realpassword", "tenantId",
                                    tenant_name="tenantName")
        except ConnectionRefused as ex:
            self.assertRaises(ex)

    def test_check_token(self):
        """ Test if I do not get any Exception while checking if a real user token is valid.
        """
        result = self.a.checkToken(self.authToken, self.token, self.tenantId)
        self.assertEqual(result, self.token)

    def test_check_already_exists(self):
        """ Test if I do not get any Exception while checking if a real user token is valid for two times.
        This test checks the token stored in memory during the second time. This time the token is expired.
        """
        result1 = self.a.checkToken(self.authToken, self.token, self.tenantId)
        result2 = self.a.checkToken(self.authToken, self.token, self.tenantId)
        self.assertEqual(result1, self.token)
        self.assertEqual(result2, self.token)

    def test_check_already_exists_and_not_expired(self):
        """ Test if I do not get any Exception while checking if a real user token is valid for two times.
        This test checks the token stored in memory during the second time. This time the token is not expired.
        """
        result1 = self.a.checkToken(self.authToken, self.token_not_expired, self.tenantId)
        result2 = self.a.checkToken(self.authToken, self.token_not_expired, self.tenantId)
        self.assertEqual(result1, self.token_not_expired)
        self.assertEqual(result2, self.token_not_expired)

    def test_check_token_exception_1(self):
        """ Test if I get an Unauthorized exception while checking if a fake user token is valid.
        """
        try:
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId)
        except Unauthorized as ex:
            self.assertRaises(ex)

    def test_check_token_exception_2(self):
        """ Test if I get an AuthorizationFailure exception while checking if a fake user token is valid but keystone
        is not responding.
        """
        try:
            self.a.identity_url = self.url_noResponse
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_check_token_exception_3(self):
        """ Test if I get an exception while checking if a fake user token is valid but keystone
        returns a server error.
        """
        try:
            self.a.identity_url = self.url_server_error
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId)
        except Exception as ex:
            self.assertRaises(ex)

    def test_check_empty_token(self):
        """ Test if I get an exception while checking if is valid an empty user token.
        """
        try:
            result = self.a.checkToken(self.authToken, "", self.tenantId)
        except Exception as ex:
            self.assertRaises(ex)

    def test_check_token_other_tenant(self):
        """ Test if I get an exception while checking if is valid a user token to access to a different tenant.
        """
        try:
            result = self.a.checkToken(self.authToken, self.token_other_tenant, self.tenantId)
        except Unauthorized as ex:
            self.assertRaises(ex)

    def test_check_token_not_found(self):
        """ Test if I get an AuthorizationFailure exception while checking if is valid a user token
        to access to a different tenant.
        """
        try:
            self.a.auth_token = self.authToken
            result = self.a.checkToken(self.authToken, self.token_not_found, self.tenantId)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_check_token_not_found_and_cached(self):
        """ Test if I get an AuthorizationFailure exception while checking if is valid a not fount user token
        in keystone but was stored in memory.
        """
        try:
            self.a.auth_token = self.authToken
            token_db = self.a.user_tokens.setdefault(self.token_not_found, {'id': self.token_not_found,
                                                        'expires': timezone.now().__str__(),
                                                         'username': self.user,
                                                         'tenant': self.tenantId,
                                                         'createdAt': timezone.now()})
            self.a.user_tokens[self.token_not_found] = token_db
            self.assertIsNotNone(self.a.get_token_from_memory(self.token_not_found))
            result = self.a.checkToken(self.authToken, self.token_not_found, self.tenantId)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_check_token_not_authorized(self):
        """ Test if I get an AuthorizationFailure exception while checking if is valid a non-authorized token.
        """
        try:
            self.a.auth_token = self.authToken
            result = self.a.checkToken(self.authToken, self.token_not_authorized, self.tenantId)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_generate_adminToken_v3(self):
        """ Test if I can generate an admin token using an AuthorizationManager with V3.
        """
        auth_manager_v3 = AuthorizationManager.AuthorizationManager(self.url_v3, AUTH_API_V3)
        auth_manager_v3.auth_token = None
        auth_manager_v3.client = self.requestsMock
        auth_manager_v3.myClient = self.mockedClient
        auth_manager_v3.session = self.session_client
        result = auth_manager_v3.get_auth_token("admin", "realpassword", "tenantId",
                                         user_domain_name="Default")
        self.assertEqual(result, self.authToken)
        self.assertEqual(auth_manager_v3.auth_token, self.authToken)

    def test_generate_adminToken_v_unsupported(self):
        """ Test if I get an exception when I try generate an admin token using an AuthorizationManager with any
        non-supported API version.
        """
        auth_manager = AuthorizationManager.AuthorizationManager(self.url_v3, AUTH_API_V3)
        auth_manager.auth_token = None
        auth_manager.api_version = "v1"
        try:
            result = auth_manager.get_auth_token("admin", "realpassword", "tenantId",
                                                 user_domain_name="Default")
        except ImportError as ex:
            self.assertRaises(ex)

    def test_check_token_v3_fail(self):
        """ Test if I get an AuthorizationFailure exception while checking if a fake user token is valid using V3.
        """
        try:
            self.a.auth_token = self.fakeToken
            self.a.api_version = AUTH_API_V3
            self.a.checkToken(self.fakeToken, self.token, self.tenantId)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)
            self.assertIsNone(self.a.auth_token)

    def test_init_auth_Manager_with_v3(self):
        """ Test if I can initialize an instance of AuthorizationManager using V3.
        """
        auth_manager = AuthorizationManager.AuthorizationManager(self.url, AUTH_API_V3)
        self.assertEqual(auth_manager.api_version, AUTH_API_V3)

    def test_check_token_v3(self):
        """ Test if I do not get any Exception while checking if a real user token is valid using V3.
        """
        self.a.api_version = AUTH_API_V3
        self.a.user_tokens.clear()
        result = self.a.checkToken(self.authToken, self.token, self.tenantId)
        self.assertEqual(result, self.token)

    def test_check_token_v3_two_times(self):
        """ Test if I do not get any Exception while checking if a real user token is valid for two times using V3.
        This test checks the token stored in memory during the second time. This time the token is expired.
        """
        self.a.api_version = AUTH_API_V3
        self.a.user_tokens.clear()

        result1 = self.a.checkToken(self.authToken, self.token, self.tenantId)
        result2 = self.a.checkToken(self.authToken, self.token, self.tenantId)

        self.assertEqual(result1, self.token)
        self.assertEqual(result2, self.token)

    def test_init_auth_Manager_with_v_unsupported(self):
        """ Test if I get an exception when I try to initialize an instance of AuthorizationManager using an
        unsupported API version.
        """
        try:
            auth_manager = AuthorizationManager.AuthorizationManager(self.url, "v1")
        except ValueError as ex:
            self.assertRaises(ex)
