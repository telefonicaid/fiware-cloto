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
from fiware_cloto.cloto.manager import AuthorizationManager

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


class MySession(MagicMock):
    # Mock of a keystone session

    def Session(self, auth, timeout):
        # Mock of the Keystone session generator
        session_mocked = mock()

        if auth.auth_url != "http://130.206.80.61:35357/v2.0":
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
        self.token = "ff01eb8a8d69418c95f0009dda9bc1852"
        self.token_other_tenant = "gg01eb8a8d69418c95f0009dda9bc1852"
        self.token_not_found = "0001eb8a8d69418c95f0009dda9bc1852"
        self.token_not_authorized = "bbbbbbba8d69418c95f0009dda9bc1852"
        self.fakeToken = "fffffffffffffffffffffffffffffffff"
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://130.206.80.61:35357/v2.0"
        self.url_noResponse = "http://127.0.0.1:35357/v2.0"
        self.url_server_error = "http://serverWithErrors.com:35357/v2.0"
        self.tenantId = "6571e3422ad84f7d828ce2f30373b3d4"
        self.a = AuthorizationManager.AuthorizationManager()
        self.mockedClient = client
        self.auth = mock()
        self.tokenM = mock()
        self.session_mocked = mock()
        self.session_client = MySession()
        manager = mock()
        requestsMock = mock()
        response = Response()
        response.status_code = HTTP_RESPONSE_CODE_OK
        response._content = '{"access":{"token":{"expires":"2015-07-09T15:16:07Z",' \
            '"id":{"token":"ff01eb8a8d69418c95f0009dda9bc1852",' \
            '"tenant":"6571e3422ad84f7d828ce2f30373b3d4","name":"user@mail.com",' \
            '"access_token":' \
            '"4HMIFCQOlswp1hZmPG-BmP6cXQWyqvIYV0WrvoKptV59O4r3_VpIJwwFx-JgJW-Lg0K_hWVmbb2ROYxnuy53jQ",' \
            '"expires":"2014-09-13T07:23:51.000Z"}' \
            ',"tenant":{"description":"Tenant from IDM","enabled":true,' \
            '"id":"6571e3422ad84f7d828ce2f30373b3d4","name":"user"}},' \
            '"user":{"username":"user","roles_links":[],"id":"user",' \
            '"roles":[{"id":"8db87ccbca3b4d1ba4814c3bb0d63aab","name":"Member"}],"name":"user"}}}'

        response_v3 = Response()
        response_v3.status_code = HTTP_RESPONSE_CODE_OK
        response_v3._content = '{"token": {"methods": ["password"], "roles": ' \
                               '[{"id": "ff01eb8a8d69418c95f0009dda9bc1852",' \
                               ' "name": "owner"}], "expires_at": "2015-05-26T13:01:49.632762Z", ' \
                               '"project": {"domain": {"id": "default", "name": "Default"},' \
                               ' "id": "6571e3422ad84f7d828ce2f30373b3d4", "name": "user@mail.com"}}}'

        response_v3_fail = Response()
        response_v3_fail.status_code = HTTP_RESPONSE_CODE_UNAUTHORIZED
        response_v3_fail._content = '{"error": {"message": "The request you have made requires authentication.",' \
                                    ' "code": 401, "title": "Unauthorized"}}'

        response2 = Response()
        response2.status_code = HTTP_RESPONSE_CODE_OK
        response2._content = '{"access":{"token":{"expires":"2015-07-09T15:16:07Z",' \
            '"id":{"token":"gg01eb8a8d69418c95f0009dda9bc1852",' \
            '"tenant":"1111e3422ad84f7d828ce2f30373b3d4","name":"user@mail.com",' \
            '"access_token":' \
            '"4HMIFCQOlswp1hZmPG-BmP6cXQWyqvIYV0WrvoKptV59O4r3_VpIJwwFx-JgJW-Lg0K_hWVmbb2ROYxnuy53jQ",' \
            '"expires":"2014-09-13T07:23:51.000Z"}' \
            ',"tenant":{"description":"Different Tenant from IDM","enabled":true,' \
            '"id":"1111e3422ad84f7d828ce2f30373b3d4","name":"user"}},' \
            '"user":{"username":"user","roles_links":[],"id":"user",' \
            '"roles":[{"id":"8db87ccbca3b4d1ba4814c3bb0d63aab","name":"Member"}],"name":"user"}}}'

        response_not_found = Response()
        response_not_found.status_code = HTTP_RESPONSE_CODE_OK
        response_not_found._content = 'User token not found'

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

        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token, headers=headers)\
            .thenReturn(response)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V3, headers=headers_v3)\
            .thenReturn(response_v3)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V3, headers=headers_v3_fake)\
            .thenReturn(response_v3_fail)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_other_tenant, headers=headers)\
            .thenReturn(response2)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_not_found, headers=headers)\
            .thenReturn(response_not_found)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.token_not_authorized, headers=headers)\
            .thenReturn(response_not_authorized)
        when(requestsMock).get(self.url + "/" + TOKENS_PATH_V2 + self.fakeToken, headers=headers)\
            .thenRaise(Unauthorized())
        when(requestsMock).get(self.url_noResponse + "/" + TOKENS_PATH_V2 + self.fakeToken, headers=headers)\
            .thenRaise(InternalServerError())
        when(requestsMock).get(self.url_server_error + "/" + TOKENS_PATH_V2 + self.token, headers=headers)\
            .thenRaise(Exception())
        self.a.client = requestsMock
        self.a.myClient = self.mockedClient
        self.a.session = self.session_client

    def test_generate_adminToken(self):

        result = self.a.get_auth_token("admin", "realpassword", "tenantId", AUTH_API_V2,
                                         self.url, tenant_name="tenantName")

        self.assertEqual(result, self.authToken)

    def test_generate_adminToken_exception(self):
        try:
            self.a.get_auth_token("admin", "fake", "tenantId", AUTH_API_V2, self.url, tenant_name="tenantName")
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_generate_adminToken_exception_2(self):
        try:
            self.a.get_auth_token("admin", "realpassword", "tenantId", AUTH_API_V2,
                                    self.url_server_error, tenant_name="tenantName")
        except ConnectionRefused as ex:
            self.assertRaises(ex)

    def test_check_token(self):
        result = self.a.checkToken(self.authToken, self.token, self.tenantId, self.url, AUTH_API_V2)
        self.assertEqual(result, None)

    def test_check_token_exception_1(self):
        try:
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId, self.url, AUTH_API_V2)
        except Unauthorized as ex:
            self.assertRaises(ex)

    def test_check_token_exception_2(self):
        try:
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId, self.url_noResponse,
                                       AUTH_API_V2)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_check_token_exception_3(self):
        try:
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId, self.url_server_error,
                                       AUTH_API_V2)
        except Exception as ex:
            self.assertRaises(ex)

    def test_check_token_exception_4(self):
        try:
            result = self.a.checkToken(self.authToken, self.fakeToken, self.tenantId, self.url, AUTH_API_V2)
        except Exception as ex:
            self.assertRaises(ex)

    def test_check_empty_token(self):
        try:
            result = self.a.checkToken(self.authToken, "", self.tenantId, self.url, AUTH_API_V2)
        except Exception as ex:
            self.assertRaises(ex)

    def test_check_token_other_tenant(self):
        try:
            result = self.a.checkToken(self.authToken, self.token_other_tenant, self.tenantId, self.url,
                                       AUTH_API_V2)
        except Unauthorized as ex:
            self.assertRaises(ex)

    def test_check_token_not_found(self):
        try:
            result = self.a.checkToken(self.authToken, self.token_not_found, self.tenantId, self.url, AUTH_API_V2)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_check_token_not_authorized(self):
        try:
            result = self.a.checkToken(self.authToken, self.token_not_authorized, self.tenantId, self.url,
                                       AUTH_API_V2)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)

    def test_generate_adminToken_v3(self):

        result = self.a.get_auth_token("admin", "realpassword", "tenantId",
                                         AUTH_API_V3, self.url,  user_domain_name="Default")

        self.assertEqual(result, self.authToken)

    def test_generate_adminToken_v_unsupported(self):
        try:
            result = self.a.get_auth_token("admin", "realpassword", "tenantId",
                                             "v4.0", self.url,  user_domain_name="Default")
        except ImportError as ex:
            self.assertRaises(ex)

    def test_check_token_v3(self):
        result = self.a.checkToken(self.authToken, self.token, self.tenantId, self.url, AUTH_API_V3)
        self.assertEqual(result, None)

    def test_check_token_v3_fail(self):
        try:
            self.a.checkToken(self.fakeToken, self.token, self.tenantId, self.url, AUTH_API_V3)
        except AuthorizationFailure as ex:
            self.assertRaises(ex)
