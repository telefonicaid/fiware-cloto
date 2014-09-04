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
from nose.tools import assert_equal

__author__ = 'gjp'
from django.test import TestCase
import datetime
import cloto.information as information
from django.test.client import RequestFactory
from mockito import *
from cloto.manager import InfoManager
from django.utils import timezone
import cloto.models as Models

from cloto.restCloto import GeneralView


class GeneralTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        info_manager = InfoManager.InfoManager()
        serverInfoMock = mock()
        tenantInfoMock = mock()
        mockedQuery = Models.ServerInfo.objects.create(
            id=1, owner="Telefonica I+D", version=1.0, runningfrom=datetime.datetime.now(
                tz=timezone.get_default_timezone()), doc="test")
        tenantQuery = Models.TenantInfo.objects.create(tenantId="tenantId", windowsize=5)
        when(serverInfoMock).objects().thenReturn(serverInfoMock)
        when(tenantInfoMock).objects().thenReturn(tenantInfoMock)
        when(serverInfoMock).get(id__exact='1').thenReturn(mockedQuery)
        when(tenantInfoMock).get(tenantId__exact="tenantId").thenReturn(tenantQuery)

        info_manager.setInformations(serverInfoMock, tenantInfoMock)
        myMock = mock()
        mockedInfo = information.information("test", "test", "test", datetime.datetime.now(), "test")
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


class WindowSizeTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        info_manager = InfoManager.InfoManager()
        serverInfoMock = mock()
        tenantInfoMock = mock()
        mockedQuery = Models.ServerInfo.objects.create(
            id=1, owner="Telefonica I+D", version=1.0, runningfrom=datetime.datetime.now(
                tz=timezone.get_default_timezone()), doc="test")
        tenantQuery = Models.TenantInfo.objects.create(tenantId="tenantId", windowsize=5)
        when(serverInfoMock).objects().thenReturn(serverInfoMock)
        when(tenantInfoMock).objects().thenReturn(tenantInfoMock)
        when(serverInfoMock).get(id__exact='1').thenReturn(mockedQuery)
        when(tenantInfoMock).get(tenantId__exact="tenantId").thenReturn(tenantQuery)

        info_manager.setInformations(serverInfoMock, tenantInfoMock)
        myMock = mock()
        mockedInfo = information.information("test", "test", "test", datetime.datetime.now(), "test")
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

    def test_not_update_window2(self):
        # Create an instance of a GET request.
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": -1}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)
