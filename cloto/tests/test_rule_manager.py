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
from cloto.models import *
from cloto.manager import RuleManager
from mockito import *
from requests import Response
from cloto.configuration import CONTEXT_BROKER_URL, NOTIFICATION_URL, NOTIFICATION_TIME, NOTIFICATION_TYPE
import uuid
import json


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.ruleUpdated = '{\"name\": \"test Name2\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.tenantId = "tenantId"
        self.serverId = "serverId"
        self.newServerId = "ServerIdThatNoExists"
        entity = Entity(serverId=self.serverId, tenantId=self.tenantId)
        entity.save()

        self.ruleManager = RuleManager.RuleManager()
        self.mockedClient = mock()
        response = Response()
        response.status_code = 200
        expected_cbSubscriptionId = "51c04a21d714fb3b37d7d5a7"
        response._content = "{\"subscribeResponse\": {" \
                            "\"duration\": \"P1M\"," \
                            "\"subscriptionId\": \"%s\"" \
                            "}" \
                            "}" % expected_cbSubscriptionId
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        #data to subscription
        data = '{"entities": [' \
               '{"type": "Server",'\
               '"isPattern": "false",' \
                          '"id": "' + self.newServerId + '"' \
                          '}],' \
                '"attributes": [' \
                            '"cpu",' \
                            '"mem"],' \
                            '"reference": "' + NOTIFICATION_URL + '/' + self.tenantId + 'servers/' + \
                            self.newServerId + '",' \
                            '"duration": "P1M",' \
                            '"notifyConditions": [' \
                            '{"type": "' + NOTIFICATION_TYPE + '",' \
                            '"condValues": ["' + NOTIFICATION_TIME + '"]}]}'
        #data2 for unsubscription
        data2 = json.dumps("{\"subscriptionId\": \"%s\"}" % expected_cbSubscriptionId)
        when(self.mockedClient).post(CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)\
            .thenReturn(response)
        when(self.mockedClient).post(CONTEXT_BROKER_URL + "/unsubscribeContext", data2, headers=headers)\
            .thenReturn(response)
        self.ruleManager.orionClient.client = self.mockedClient

        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)

    def test_get_rule_info(self):
        """Tests if method returns information about a general rule."""
        r_model = RuleManager.RuleManager().get_rule_model()
        self.assertEqual(RuleModel, r_model)

    def test_create_get_delete_rule(self):
        """Tests lifecycle of a general rule, creating a rule, checking if it was created and deleting it."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_rule(rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_rule(rule.ruleId)
        self.assertEqual(response, True)

    def test_create_rule_and_update(self):
        """Tests if method creates a general rule."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        updated = RuleManager.RuleManager().update_rule(self.tenantId, rule.ruleId, self.rule)
        self.assertIsInstance(updated, RuleModel)
        self.assertIsNotNone(updated.ruleId)

    def test_get_all_rules(self):
        """Tests if method list all general rules of a tenant."""
        rules = RuleManager.RuleManager().get_all_rules(self.tenantId)
        self.assertIsInstance(rules, ListRuleModel)

    def test_create_get_delete_specific_rule(self):
        """Tests lifecycle of a specific rule, creating a rule, checking if it was created and deleting it."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_specific_rule(self.tenantId, self.serverId, rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_specific_rule(self.tenantId, self.serverId, rule.ruleId)
        self.assertEqual(response, True)

    def test_create_specific_rule_for_new_server_and_updating(self):
        """Tests if method creates the first specific rule for a server and update it with other information."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        update = RuleManager.RuleManager().update_specific_rule(
            self.tenantId, self.newServerId, rule.ruleId, self.ruleUpdated)
        self.assertIsInstance(update, RuleModel)
        self.assertIsNotNone(update.ruleId)

    def test_get_all_specific_rules(self):
        """Tests if method list all general rules of a server."""
        rules = RuleManager.RuleManager().get_all_specific_rules(self.tenantId, self.serverId)
        self.assertIsInstance(rules, ListRuleModel)

    def test_suscription_get_subscription_and_unsuscribe_to_a_rule_(self):
        """Tests if method subscribes a server to a rule, gets the subscription and unsubsribes the server."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        subscrp = RuleManager.RuleManager().get_subscription(self.tenantId, self.newServerId, subscriptionId)
        self.assertIsInstance(subscrp, SubscriptionModel)
        self.assertEqual(url, subscrp.url)

        result = self.ruleManager.unsubscribe_to_rule(self.newServerId, subscriptionId)
        self.assertIs(result, True)
