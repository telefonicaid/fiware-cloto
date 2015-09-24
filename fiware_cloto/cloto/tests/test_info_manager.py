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
from fiware_cloto.cloto.manager import InfoManager

__author__ = 'gjp'
import datetime

from django.test import TestCase
from mockito import mock, when
from django.utils import timezone

from fiware_cloto.cloto.manager import InfoManager
from fiware_cloto.cloto.models import TenantInfo, ServerInfo


class InfoManagerTests(TestCase):
    def setUp(self):
        self.info = InfoManager.InfoManager()
        self.tenantId = "tenantId"
        self.originalSize = 5
        self.newSize = 4
        self.tenantInfoMocked = mock()
        self.serverInfoMocked = mock()
        mockedQuery = TenantInfo.objects.create(tenantId=self.tenantId, windowsize=self.originalSize)
        when(self.tenantInfoMocked).get(tenantId__exact=self.tenantId).thenReturn(mockedQuery)
        when(self.tenantInfoMocked).obects().thenReturn(self.tenantInfoMocked)
        serverQuery = ServerInfo.objects.create(id=1, owner="Telefonica I+D", version=1.0,
            runningfrom=datetime.datetime.now(tz=timezone.get_default_timezone()), doc="test")

    def test_get_server_information_model(self):
        s_model = self.info.get_server_information()
        self.assertEqual(ServerInfo, s_model)

    def test_get_tenant_information_model(self):
        t_model = self.info.get_tenant_information()
        self.assertEqual(TenantInfo, t_model)
