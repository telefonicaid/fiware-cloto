__author__ = 'gjp'
from django.test import TestCase
from cloto.models import *
from cloto.manager import RuleManager
import uuid


class RuleManagerTests(TestCase):
    def setUp(self):
        self.rule = "{\"name\": \"test Name\", \"condition\": \"test Condition\",\"action\": \"test Action\"}"
        self.ruleUpdated = "{\"name\": \"test Name2\", \"condition\": \"test Condition\",\"action\": \"test Action\"}"
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


    def test_create_rule_and_update(self):
        """Tests if method creates a general rule."""
        rule = RuleManager.RuleManager().create_general_rule(self.tenantId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        updated = RuleManager.RuleManager().update_rule(rule.ruleId, self.rule)
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

        rule2 = RuleManager.RuleManager().get_specific_rule(rule.ruleId)
        self.assertIsInstance(rule2, RuleModel)
        self.assertIsNotNone(rule2.ruleId)

        response = RuleManager.RuleManager().delete_specific_rule(self.serverId, rule.ruleId)
        self.assertEqual(response, True)

    def test_create_specific_rule_for_new_server_and_updating(self):
        """Tests if method creates the first specific rule for a server and update it with other information."""
        rule = RuleManager.RuleManager().create_specific_rule(self.tenantId, self.newServerId, self.rule)
        self.assertIsInstance(rule, RuleModel)
        self.assertIsNotNone(rule.ruleId)

        update = RuleManager.RuleManager().update_specific_rule(rule.ruleId, self.ruleUpdated)
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
        url = "http://URL:PORT/testService"
        subscription = "{\"url\": \"http://URL:PORT/testService\", \"ruleId\": \"%s\"}" % rule.ruleId

        subscriptionId = RuleManager.RuleManager().subscribe_to_rule(self.tenantId, self.serverId, subscription)
        self.assertIsInstance(subscriptionId, uuid.UUID)

        subscrp = RuleManager.RuleManager().get_subscription(self.tenantId, self.serverId, subscriptionId)
        self.assertIsInstance(subscrp, SubscriptionModel)
        self.assertEqual(url, subscrp.url)

        result = RuleManager.RuleManager().unsubscribe_to_rule(subscriptionId)
        self.assertIs(result, True)

