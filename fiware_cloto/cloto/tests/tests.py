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

from unittest import skip
from django.test import TestCase
from django.test.client import RequestFactory
from mockito import mock, when
from mock import patch
from fiware_cloto.cloto.manager import InfoManager
from fiware_cloto.cloto import information
from fiware_cloto.cloto.restCloto import GeneralView
import fiware_cloto.cloto.models as Models
import json


class GeneralTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        info_manager = InfoManager.InfoManager()
        info_manager.init_information()
        serverInfoMock = mock()
        tenantInfoMock = mock()
        #mockedQuery = Models.ServerInfo.objects.create(
        #    id=1, owner="Telefonica I+D", version=1.0, runningfrom=datetime.datetime.now(
        #        tz=timezone.get_default_timezone()), doc="test")
        tenantQuery = Models.TenantInfo.objects.create(tenantId="tenantId", windowsize=5)
        when(serverInfoMock).objects().thenReturn(serverInfoMock)
        when(tenantInfoMock).objects().thenReturn(tenantInfoMock)
        #when(serverInfoMock).get(id__exact='1').thenReturn(mockedQuery)
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
        info_manager.init_information()
        serverInfoMock = mock()
        tenantInfoMock = mock()
        tenantQuery = Models.TenantInfo.objects.create(tenantId="tenantId", windowsize=5)
        when(serverInfoMock).objects().thenReturn(serverInfoMock)
        when(tenantInfoMock).objects().thenReturn(tenantInfoMock)
        when(tenantInfoMock).get(tenantId__exact="tenantId").thenReturn(tenantQuery)
        info_manager.setInformations(serverInfoMock, tenantInfoMock)
        myMock = mock()
        mockedInfo = information.information("test", "test", "test", datetime.datetime.now(), "test")
        validWindowSize = "4"
        self.validWindowSizeValue = 5
        self.new_windowsize_value = 4
        invalidWindowSize = "notValidValue"
        when(myMock).updateWindowSize("tenantId", self.validWindowSizeValue).thenReturn(mockedInfo)
        when(myMock).updateWindowSize("tenantId", invalidWindowSize).thenReturn(None)

        when(myMock).parse("{\"windowsize\": %s}" % validWindowSize).thenReturn(mockedInfo)
        when(myMock).parse("{\"windowsize\": %s}" % invalidWindowSize).thenReturn(None)
        self.general = GeneralView()

    @patch('fiware_cloto.cloto.manager.InfoManager.logger')
    @patch('fiware_cloto.cloto.manager.InfoManager.pika')
    def test_update_window(self, mock_pika, mock_logging):
        """Test if server updates the window size of a tenant.
        """
        request_check_init = self.factory.get('/v1.0/tenantId/')
        response_check_init = self.general.GET(request_check_init, "tenantId")

        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": " + str(self.new_windowsize_value)
                                   + "}", "application/json")

        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 200)

        request_check_final = self.factory.get('/v1.0/tenantId/')
        response_check_final = self.general.GET(request_check_final, "tenantId")

        window_size_init = json.loads(response_check_init.content)["windowsize"]
        window_size_final = json.loads(response_check_final.content)["windowsize"]

        self.assertEqual(window_size_init, self.validWindowSizeValue)
        self.assertEqual(window_size_final, self.new_windowsize_value)

        self.assertTrue(mock_logging.info.called)
        self.assertTrue(mock_pika.BlockingConnection.called)

    @patch('fiware_cloto.cloto.manager.InfoManager.logger')
    def test_update_window_fail_connection(self, mock_logging):
        """Test if Publish a message related to the windowsize in the rabbitmq fails when there is
        no connection to rabbit.
        """
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": " + str(self.new_windowsize_value)
                                   + "}", "application/json")

        try:
            response = self.general.PUT(request, "tenantId")
        except Exception as ex:
            self.assertRaises(ex)
        self.assertTrue(mock_logging.info.called)

    def test_not_update_window(self):
        """test_not_update_window check that PUT windowsize fails with error 400 when an invalid
        value is provided in the request"""
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": notValidValue}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)

    def test_not_update_window2(self):
        """test_not_update_window2 check that PUT windowsize fails with error 400 when an invalid
        numeric value is provided in the request"""

        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": -1}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)

    def test_not_update_window_size_with_string(self):
        """test_not_update_window_size_with_string check that PUT windowsize fails with error 400 when an invalid
        string is provided in the request
        """
        request = self.factory.put('/v1.0/tenantId/', "{\"windowsize\": \"zero\"}", "application/json")

        # Test my_view() as if it were deployed at /customer/details
        response = self.general.PUT(request, "tenantId")
        self.assertEqual(response.status_code, 400)

    @skip
    def testPublishingConnectionNone(self):
        """ Test if method fails when tries to publish a message with AMQP connection equal to None.
        """
        queue = InfoManager.InfoManager()

        queue.connection = None

        expectedvalue = "AMQP connection not properly created..."

        message = "tenantId " + str(self.validWindowSizeValue)

        try:
            queue.publish_message(message)
        except (Exception), err:
            self.assertEqual(expectedvalue, err.message)
