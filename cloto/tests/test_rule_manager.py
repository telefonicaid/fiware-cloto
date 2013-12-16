__author__ = 'gjp'
from django.test import TestCase
from cloto.models import *
from cloto.manager import RuleManager


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = "{\"condition\": \"test Condition\",\"action\": \"test Action\"}"
        self.tenantId = "tenantId"

    def test_get_rule_info(self):
        r_model = RuleManager.RuleManager().get_rule_model()
        self.assertEqual(RuleModel, r_model)

    def test_create_and_get_rule(self):
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_rule(rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

    def test_create_rule(self):
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

    def test_get_all_rules(self):
        rules = RuleManager.RuleManager().get_all_rules(self.tenantId)
        self.assertIsInstance(rules, ListRuleModel)
