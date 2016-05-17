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
from django.test import TestCase, Client
from mockito import mock, when
from keystoneclient.v2_0 import client
from keystoneclient.exceptions import AuthorizationFailure

from fiware_cloto.cloto.manager import AuthorizationManager


class ClientTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.authToken = "77d254b3caba4fb29747958138136ffa"
        self.url = "http://130.206.80.61:35357/v2.0"
        self.mockedClient = client
        self.auth = mock()
        self.auth.stub("authenticate")
        self.auth.__setattr__("auth_token", self.authToken)
        when(self.auth.stub("tokens")).authenticate(token="1234").thenReturn(True)
        when(AuthorizationManager.AuthorizationManager)\
            .checkToken(None, "1234", "tenantId").thenReturn(True)
        when(AuthorizationManager.AuthorizationManager)\
            .checkToken(None, "12345", "tenantId").thenRaise(AuthorizationFailure())
        when(AuthorizationManager.AuthorizationManager).\
            get_auth_token("admin", "openstack").thenReturn(self.authToken)

    def test_servers_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/', **{'HTTP_X_AUTH_TOKEN': '1234'})

    def test_server_rules_view_url(self):
        response = self.c.get('/v1.0/tenantId/servers/rules', **{'HTTP_X_AUTH_TOKEN': '1234'})

    def test_tenant_info_view_url_fail(self):
        """ Test if using an invalid token to access tenant_info resource returns an AuthorizationFailure Exception.
        """
        try:
            response = self.c.get('/v1.0/tenantId', **{'HTTP_X_AUTH_TOKEN': '12345'})
        except AuthorizationFailure as ex:
            self.assertRaises(ex)
