__author__ = 'gjp'
import datetime
import json
import uuid
from cloto.models import Rule, RuleModel, ListRuleModel, Entity, SpecificRule
from django.utils import timezone


class RuleManager():
    """This class provides methods to manage rules.
    """

    def get_rule_model(self):
        """Returns model of Rule."""
        return RuleModel

    def get_rule(self, ruleId):
        """Returns information about a general rule."""
        r_query = Rule.objects.get(ruleId__exact=ruleId)
        rule = RuleModel()
        rule.ruleId = r_query.__getattribute__("ruleId")
        rule.name = r_query.__getattribute__("name")
        rule.condition = r_query.__getattribute__("condition")
        rule.action = r_query.__getattribute__("action")
        return rule

    def delete_rule(self, ruleId):
        """Returns information about a general rule."""
        r_query = Rule.objects.get(ruleId__exact=ruleId)
        r_query.delete()
        return True

    def get_all_rules(self, tenantId):
        """Returns all general rules of a tenant."""
        dict = list(Rule.objects.filter(tenantId=tenantId).values('ruleId', 'name', 'condition', 'action'))

        mylist = ListRuleModel()
        mylist.tenantId = tenantId
        mylist.rules = dict

        return mylist

    def create_general_rule(self, tenantId, rule):
        """Creates new general rule """
        condition = self.getContition(rule)
        action = self.getAction(rule)
        name = self.getName(rule)
        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = Rule(ruleId=ruleId, tenantId=tenantId,
                    name=name, condition=condition, action=action, createdAt=createdAt)
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

    def getName(self, rule):
        """Splits the name from a rule."""
        name = json.loads(rule)['name']
        return name

    def create_specific_rule(self, tenantId, serverId, rule):
        """Creates new specific rule for a server."""
        try:
            entity = Entity.objects.get(entity_Id__exact=serverId)
        except Entity.DoesNotExist as err:
            entity = Entity(entity_Id=serverId, tenantId=tenantId)
            entity.save()

        condition = self.getContition(rule)
        action = self.getAction(rule)
        name = self.getName(rule)
        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = SpecificRule(specificRule_Id=ruleId,
                            tenantId=tenantId, name=name, condition=condition, action=action, createdAt=createdAt)
        rule.save()
        entity.specificrules.add(rule)
        rule.save()
        return ruleId
