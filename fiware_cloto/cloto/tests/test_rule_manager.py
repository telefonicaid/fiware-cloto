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
import uuid
import json
from fiware_cloto.cloto.models import RuleModel, Entity, ListRuleModel, SubscriptionModel, SpecificRule
from django.test import TestCase
from keystoneclient.exceptions import Conflict
from mockito import mock, when
from mock import patch
from requests import Response
from django.conf import settings

from fiware_cloto.cloto.manager import RuleManager


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"hdd\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"net\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.ruleUpdated = '{\"name\": \"test Name2\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"hdd\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"net\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-email\", \"body\": \"test body\",' \
                    ' \"email\": \"test@host.com\"}}'
        self.ruleFake1 = '{\"name\": \"te\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.ruleFake2 = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": \"\"}'
        self.ruleFake3 = '{\"name\": \"test Name\", \"condition\": \"\",' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.ruleFake4 = '{\"name\": \"test Name\",' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'

        self.tenantId = "tenantId"
        self.serverId = "serverId"
        self.newServerId = "ServerIdThatNoExists"
        entity = Entity(serverId=self.serverId, tenantId=self.tenantId)
        entity.save()
        CONTEXT_BROKER_URL_FAIL = "http://130.206.82.0:1026/NGSI10"
        self.ruleManager = RuleManager.RuleManager()
        self.mockedClient = mock()
        self.OrionClientError = mock()
        response = Response()
        responseFailure = Response()
        self.subscription_failure = "{Invalid subscription body}"
        responseFailure.status_code = 400
        response.status_code = 200
        self.expected_cbSubscriptionId = "51c04a21d714fb3b37d7d5a7"
        response._content = "{\"subscribeResponse\": {" \
                            "\"duration\": \"P1M\"," \
                            "\"subscriptionId\": \"%s\"" \
                            "}" \
                            "}" % self.expected_cbSubscriptionId
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
                            '"reference": "' + settings.NOTIFICATION_URL + '/' + self.tenantId + 'servers/' + \
                            self.newServerId + '",' \
                            '"duration": "P1M",' \
                            '"notifyConditions": [' \
                            '{"type": "' + settings.NOTIFICATION_TYPE + '",' \
                            '"condValues": ["' + settings.NOTIFICATION_TIME + '"]}]}'
        #data2 for unsubscription
        data2 = json.dumps("{\"subscriptionId\": \"%s\"}" % self.expected_cbSubscriptionId)
        when(self.mockedClient).post(settings.CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)\
            .thenReturn(response)
        when(self.mockedClient).post(settings.CONTEXT_BROKER_URL + "/unsubscribeContext", data2, headers=headers)\
            .thenReturn(response)
        when(self.OrionClientError).post(settings.CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)\
            .thenReturn(responseFailure)
        when(self.OrionClientError).post(settings.CONTEXT_BROKER_URL + "/unsubscribeContext", data2, headers=headers)\
            .thenReturn(responseFailure)
        self.ruleManager.orionClient.client = self.mockedClient

        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)

    def test_get_rule_info(self):
        """Test if method returns information about a general rule."""
        r_model = RuleManager.RuleManager().get_rule_model()
        self.assertEqual(RuleModel, r_model)

    def test_create_get_delete_rule(self):
        """Test lifecycle of a general rule, creating a rule, checking if it was created and deleting it."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_rule(rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_rule(rule.ruleId)
        self.assertEqual(response, True)

    def test_create_rule_and_update(self):
        """Test if method creates a general rule."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        updated = RuleManager.RuleManager().update_rule(self.tenantId, rule.ruleId, self.rule)
        self.assertIsInstance(updated, RuleModel)
        self.assertIsNotNone(updated.ruleId)

    def test_create_general_rule_incomplete(self):
        """Test if create general rule throws error with malformed rule, condition is missing."""
        try:
            rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.ruleFake4)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_create_rule_and_update_fake_rule(self):
        """Test if update a rule throws error with malformed rule, one attribute is missing."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        try:
            updated = RuleManager.RuleManager().update_rule(self.tenantId, rule.ruleId, self.ruleFake4)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_get_all_rules(self):
        """Test if method list all general rules of a tenant."""
        rules = RuleManager.RuleManager().get_all_rules(self.tenantId)
        self.assertIsInstance(rules, ListRuleModel)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_create_get_delete_specific_rule(self, mock_logging):
        """Test lifecycle of a specific rule, creating a rule, checking if it was created and deleting it."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_specific_rule(self.tenantId, self.serverId, rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_specific_rule(self.tenantId, self.serverId, rule.ruleId)
        self.assertEqual(response, True)
        self.assertTrue(mock_logging.info.called)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_create_specific_rule_for_new_server_and_updating(self, mock_logging):
        """Test if method creates the first specific rule for a server and update it with other information."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        update = RuleManager.RuleManager().update_specific_rule(
            self.tenantId, self.newServerId, rule.ruleId, self.ruleUpdated)
        self.assertIsInstance(update, RuleModel)
        self.assertIsNotNone(update.ruleId)
        self.assertTrue(mock_logging.info.called)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_create_specific_rule_for_new_server_and_updating_with_fake_rule(self, mock_logging):
        """Test if method creates the first rule for a server and fails when update it with fake information."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        try:
            update = RuleManager.RuleManager().update_specific_rule(
            self.tenantId, self.newServerId, rule.ruleId, self.ruleFake4)
        except ValueError as ex:
            self.assertRaises(ex)
        self.assertTrue(mock_logging.info.called)

    def test_validate_rule_error_1(self):
        """Test if method throws error with malformed rule, name lenght is 2. """
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.ruleFake1)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_validate_rule_error_2(self):
        """Test if method throws error with malformed rule, action is empty."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.ruleFake2)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_validate_rule_error_3(self):
        """Test if method throws error with malformed rule, condition is empty."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.ruleFake3)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_validate_rule_error_4(self):
        """Test if method throws error with malformed rule, one attribute is missing."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.ruleFake4)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_get_all_specific_rules(self):
        """Test if method list all general rules of a server."""
        rules = RuleManager.RuleManager().get_all_specific_rules(self.tenantId, self.serverId)
        self.assertIsInstance(rules, ListRuleModel)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_get_all_entities(self, mock_logging):
        """Test if method creates a rule for a server and gets all information about all servers."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        self.assertTrue(mock_logging.info.called)

        listRules = RuleManager.RuleManager().get_all_entities(self.tenantId)
        self.assertIsInstance(listRules, ListRuleModel)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_suscription_get_subscription_and_unsuscribe_to_a_rule_(self, mock_logging):
        """Test if method subscribes a server to a rule, gets the subscription and unsubscribes the server."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        self.assertTrue(mock_logging.info.called)
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        subscrp = RuleManager.RuleManager().get_subscription(self.tenantId, self.newServerId, subscriptionId)
        self.assertIsInstance(subscrp, SubscriptionModel)
        self.assertEqual(url, subscrp.url)

        result = self.ruleManager.unsubscribe_to_rule(self.newServerId, subscriptionId)
        self.assertIs(result, True)

    def test_suscription_server_no_exists(self):
        """Test if method subscribes_fails_with_fake_rule_id."""
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"1234\"}"
        try:
            self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        except SpecificRule.DoesNotExist as ex:
            self.assertRaises(ex)

    def test_double_subscription(self):
        """Test if method throws an error trying to subcribe a server to a rule twice."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        try:
            subscriptionId2 = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        except Conflict as ex:
            self.assertRaises(ex)

    def test_unsubscription_Orion_Failure(self):
        """Test if method throws an error when Orion response is 400 while we are unsubscribing a server."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        self.ruleManager.orionClient.client = self.OrionClientError

        try:
            result = self.ruleManager.unsubscribe_to_rule(self.newServerId, subscriptionId)
        except SystemError as ex:
            self.assertRaises(ex)

    def test_subscription_Orion_Failure(self):
        """Test if method throws an error when Orion response is 400 while we are subscribing a server."""
        self.ruleManager.orionClient.client = self.OrionClientError
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        url = "http://127.0.0.1:8000/testService"
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId
        try:
            self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        except SystemError as ex:
            self.assertRaises(ex)

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_double_suscription_with_different_rules_and_unsubscription(self, mock_logging,):
        """Test if method subscribes a server to a rule, and use the same subscriptions for more rules."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        rule2 = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.ruleUpdated)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)
        subscription = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        subscription2 = "{\"url\": \"http://127.0.0.1:8000/testService\", \"ruleId\": \"%s\"}" % rule2.ruleId
        subscriptionId2 = self.ruleManager.subscribe_to_rule(self.tenantId, self.newServerId, subscription2)
        self.assertIsInstance(subscriptionId2, uuid.UUID)

        """Test if method list all rules of a server."""
        rules = RuleManager.RuleManager().get_all_specific_rules(self.tenantId, self.newServerId)
        self.assertIsInstance(rules, ListRuleModel)

        result = self.ruleManager.unsubscribe_to_rule(self.newServerId, subscriptionId2)
        self.assertIs(result, True)
        self.assertTrue(mock_logging.info.called)
