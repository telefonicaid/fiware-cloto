__author__ = 'gjp'
from django.test import TestCase
from cloto.models import *
from cloto.manager import RuleManager


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = "{\"name\": \"test Name\", \"condition\": \"test Condition\",\"action\": \"test Action\"}"
        self.tenantId = "tenantId"
        self.serverId = "serverId"
        self.newServerId = "ServerIdThatNoExists"
        entity = Entity(entity_Id=self.serverId, tenantId=self.tenantId)
        entity.save()
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


    def test_create_rule(self):
        """Tests if method creates a general rule."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

    def test_get_all_rules(self):
        """Tests if method list all general rules of a tenant."""
        rules = RuleManager.RuleManager().get_all_rules(self.tenantId)
        self.assertIsInstance(rules, ListRuleModel)

    def test_create_get_delete_specific_rule(self):
        """Tests lifecycle of a specific rule, creating a rule, checking if it was created and deleting it."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.serverId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        rule2 = RuleManager.RuleManager().get_specific_rule(rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_specific_rule(self.serverId, rule.ruleId)
        self.assertEqual(response, True)

    def test_create_specific_rule_for_new_server(self):
        """Tests if method creates the first specific rule for a server."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)


    def test_get_all_specific_rules(self):
        """Tests if method list all general rules of a server."""
        rules = RuleManager.RuleManager().get_all_specific_rules(self.tenantId, self.serverId)
        self.assertIsInstance(rules, ListRuleModel)