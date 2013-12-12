__author__ = 'gjp'
import datetime
import json
import uuid
from cloto.models import Rule, RuleModel, ListRuleModel
from django.utils import timezone


class RuleManager():
    """This class provides methods to manage rules.
    """

    def get_rule_model(self):
        """Returns model of Rule."""
        return RuleModel

    def get_rule(self, ruleId):
        """Returns information about a rule."""
        r_query = Rule.objects.get(ruleId__exact=ruleId)
        rule = RuleModel()
        rule.ruleId = r_query.__getattribute__("ruleId")
        rule.condition = r_query.__getattribute__("condition")
        rule.action = r_query.__getattribute__("action")
        return rule

    def get_all_rules(self, tenantId):
        """Returns all rules of a tenant."""
        dict = list(Rule.objects.filter(tenantId=tenantId).values('ruleId', 'condition', 'action'))

        mylist = ListRuleModel()
        mylist.tenantId = tenantId
        mylist.rules = dict

        return mylist

    def create_general_rule(self, tenantId, rule):
        """Creates new general rule """
        condition = self.getContition(rule)
        action = self.getAction(rule)
        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = Rule(ruleId=ruleId, tenantId=tenantId, condition=condition, action=action, createdAt=createdAt)
        rule.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        return ruleResult

    def getContition(self, rule):
        """Splits contitions from a rule."""
        condition = json.loads(rule)['condition']
        return condition

    def getAction(self, rule):
        """Splits action from a rule."""
        action = json.loads(rule)['action']
        return action
