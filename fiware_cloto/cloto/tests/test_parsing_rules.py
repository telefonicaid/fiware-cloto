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
from mock import patch

from fiware_cloto.cloto.manager import RuleManager
from fiware_cloto.cloto.models import RuleModel


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"hdd\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"net\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.rule_without_operation = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\"}}'
        self.rule_empty_actionname = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"\", \"operation\": \"scaleUp\"}}'
        self.rule_without_actionname = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"operation\": \"scaleUp\"}}'
        self.rule_operation_unknown = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 98, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"unknown\"}}'
        self.rule_cpu_overlimit = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 101, \"operand\": \"greater\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.rule_operand_unknown = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"cpu\": {\"value\": 101, \"operand\": \"unknown\"},' \
                    ' \"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'
        self.rule_condition_parameter_missing = '{\"name\": \"test Name\", \"condition\": ' \
                    '{\"mem\": {\"value\": 95, \"operand\": \"greater equal\"}},' \
                    '\"action\": {\"actionName\": \"notify-scale\", \"operation\": \"scaleUp\"}}'

        self.tenantId = "tenantId"
        self.serverId = "serverId"

    @patch('fiware_cloto.cloto.manager.RuleManager.logger')
    def test_pimp_rule(self, mock_logging):
        """Test if method creates the first rule for a server and fails when update it with fake information."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)
        self.assertTrue(mock_logging.info.called)

    def test_pimp_rule_error_1(self):
        """Test if method throws error with malformed rule without action name."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_without_actionname)
        except KeyError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_error_2(self):
        """Test if method throws error with malformed rule without operation."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_without_operation)
        except KeyError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_error_3(self):
        """Test if method throws error with malformed rule with an empty action name."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_empty_actionname)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_error_4(self):
        """Test if method throws error with malformed rule with an unknown operation."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_operation_unknown)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_error_5(self):
        """Test if method throws error with malformed rule, CPU has value over 100"""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_cpu_overlimit)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_error_6(self):
        """Test if method throws error with malformed rule with an unknown operand. """
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule_operand_unknown)
        except ValueError as ex:
            self.assertRaises(ex)

    def test_pimp_rule_condition_error_1(self):
        """Test if method throws error with malformed rule, with a missing parameter in the condition."""
        try:
            RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId,
                                                           self.rule_condition_parameter_missing)
        except KeyError as ex:
            self.assertRaises(ex)
