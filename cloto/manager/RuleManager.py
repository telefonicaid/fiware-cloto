__author__ = 'gjp'
import datetime
import json
import uuid
from cloto.models import Rule, RuleModel, ListRuleModel, Entity, SpecificRule, Subscription, SubscriptionModel
from django.utils import timezone
from django.core.validators import URLValidator
from keystoneclient.exceptions import Conflict
import cloto.OrionClient as OrionClient


class RuleManager():
    """This class provides methods to manage rules.
    """
    #ContextBrokerClient
    orionClient = OrionClient.OrionClient()

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
        """Deletes a general rule."""
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
        try:
            condition = self.getContition(rule)
            action = self.getAction(rule)
            name = self.getName(rule)
        except Exception as err:
            raise ValueError(str(err) + " is missing")

        self.checkRule(name, condition, action)

        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = Rule(ruleId=ruleId, tenantId=tenantId,
                    name=name, condition=condition, action=action, createdAt=createdAt)
        rule.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        return ruleResult

    def update_rule(self, tenantId, ruleId, rule):
        """Updates a general rule """
        rule_db = Rule.objects.get(ruleId__exact=ruleId, tenantId__exact=tenantId)

        try:
            condition = self.getContition(rule)
            action = self.getAction(rule)
            name = self.getName(rule)
        except Exception as err:
            raise ValueError(str(err) + " is missing")

        self.checkRule(name, condition, action)

        rule_db.action = action
        rule_db.name = name
        rule_db.condition = condition
        rule_db.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        ruleResult.name = name
        ruleResult.condition = condition
        ruleResult.action = action
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
            entity = Entity.objects.get(serverId__exact=serverId)
        except Entity.DoesNotExist as err:
            entity = Entity(serverId=serverId, tenantId=tenantId)
            entity.save()
        try:
            condition = self.getContition(rule)
            action = self.getAction(rule)
            name = self.getName(rule)
        except Exception as err:
            raise ValueError(str(err) + " is missing")

        self.checkRule(name, condition, action)

        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = SpecificRule(specificRule_Id=ruleId,
                            tenantId=tenantId, name=name, condition=condition, action=action, createdAt=createdAt)
        """try:
            rule = SpecificRule.objects.get(serverId__exact=serverId, )
            raise ValueError("rule name already exists")
        except Entity.DoesNotExist as err:
            entity = Entity(serverId=serverId, tenantId=tenantId)"""
        rule.save()
        entity.specificrules.add(rule)
        rule.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        return ruleResult

    def update_specific_rule(self, tenantId, serverId, ruleId, rule):
        """Updates a general rule """
        rule_db = SpecificRule.objects.get(specificRule_Id__exact=ruleId,
                                           tenantId__exact=tenantId, entity__exact=serverId)
        try:
            condition = self.getContition(rule)
            action = self.getAction(rule)
            name = self.getName(rule)
        except Exception as err:
            raise ValueError(str(err) + " is missing")

        self.checkRule(name, condition, action)

        rule_db.action = action
        rule_db.name = name
        rule_db.condition = condition
        rule_db.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        ruleResult.name = name
        ruleResult.condition = condition
        ruleResult.action = action
        return ruleResult

    def get_specific_rule(self, tenantId, serverId, ruleId):
        """Returns information about a specific rule."""
        r_query = SpecificRule.objects.get(specificRule_Id__exact=ruleId,
                                           tenantId__exact=tenantId, entity__exact=serverId)
        rule = RuleModel()
        rule.ruleId = r_query.__getattribute__("specificRule_Id")
        rule.name = r_query.__getattribute__("name")
        rule.condition = r_query.__getattribute__("condition")
        rule.action = r_query.__getattribute__("action")
        return rule

    def get_all_specific_rules(self, tenantId, serverId):
        """Returns all specific rules of a server."""
        entity = Entity.objects.get(serverId=serverId)

        mylist = entity.specificrules.values('specificRule_Id', 'name', 'condition', 'action').iterator()

        dictRules = list()
        for rule in mylist:
            dictRules.append(rule)
        subscr = entity.subscription.values('subscription_Id', 'ruleId').iterator()
        dictSubsc = list()
        for subs in subscr:
            dictSubsc.append(subs)

        mylist = ListRuleModel()
        mylist.tenantId = tenantId
        mylist.rules = dictRules
        mylist.serverId = serverId
        mylist.subscription = dictSubsc

        return mylist

    def delete_specific_rule(self, tenantId, serverId, ruleId):
        """Deletes a specific rule."""
        r_query = SpecificRule.objects.get(specificRule_Id__exact=ruleId,
                                           tenantId__exact=tenantId, entity__exact=serverId)
        r_query.delete()

        #Deleting subscriptions to that rule
        subscriptions = Subscription.objects.filter(ruleId__exact=ruleId)
        subscriptions.delete()
        return True

    def get_all_entities(self, tenantId):
        """Returns all servers with their information."""
        servers = Entity.objects.filter(tenantId__exact=tenantId).values('serverId').iterator()
        dictEntities = list()
        for entity in servers:
            s = entity['serverId']
            rules = self.get_all_specific_rules(tenantId, s)
            for rule in rules.rules:
                del rule['action']
                del rule['condition']

            final = ListRuleModel()
            final.rules = rules.rules
            final.serverId = rules.serverId
            dictEntities.append(vars(final))

        mylist = ListRuleModel()
        mylist.servers = dictEntities

        return mylist

    def subscribe_to_rule(self, tenantId, serverId, subscription):
        """Creates a server subscription to a rule """
        context_broker_subscription = False
        try:
            entity = Entity.objects.get(serverId__exact=serverId)
        except Entity.DoesNotExist as err:
            entity = Entity(serverId=serverId, tenantId=tenantId)
            entity.save()

        ruleId = json.loads(subscription)['ruleId']
        SpecificRule.objects.get(specificRule_Id__exact=ruleId, entity__exact=serverId)
        url = json.loads(subscription)['url']

        #Verify that there is no more subscriptions to the rule for that server
        it = entity.subscription.iterator()
        for sub in it:
            if sub.serverId == serverId:
                context_broker_subscription = True
            if sub.ruleId == ruleId:
                raise Conflict("Subscription already exists")

        self.verify_url(url)
        if not context_broker_subscription:
            cbSubscriptionId = self.orionClient.contextBrokerSubscription(tenantId, serverId)
        subscription_Id = uuid.uuid1()
        subscr = Subscription(subscription_Id=subscription_Id, ruleId=ruleId, url=url, serverId=serverId,
                              cbSubscriptionId=cbSubscriptionId)
        subscr.save()
        entity.subscription.add(subscr)
        entity.save()

        return subscription_Id

    def unsubscribe_to_rule(self, serverId, subscriptionId):
        """Unsuscribe a server from a rule """

        r_query = Subscription.objects.get(subscription_Id__exact=subscriptionId, serverId__exact=serverId)
        if Subscription.objects.filter(serverId__exact=serverId).count() == 1:
            self.orionClient.contextBrokerUnSubscription(r_query.cbSubscriptionId, r_query.serverId)
            r_query.delete()
        else:
            r_query.delete()
        return True

    def get_subscription(self, tenantId, serverId, subscriptionId):
        """Returns information about a subscription."""
        r_query = Subscription.objects.get(subscription_Id__exact=subscriptionId, serverId__exact=serverId)
        subscription = SubscriptionModel()
        subscription.ruleId = r_query.__getattribute__("ruleId")
        subscription.serverId = r_query.__getattribute__("serverId")
        subscription.url = r_query.__getattribute__("url")
        subscription.subscriptionId = r_query.__getattribute__("subscription_Id")
        return subscription

    def checkRule(self, name, condition, action):

        if name.__len__() > 30 or name.__len__() < 3:
            raise ValueError("You must provide a name with length between 3 and 30 characters")
        if condition.__len__() > 1024 or condition.__len__() < 1:
            raise ValueError("You must provide conditions with length between 1 and 1024 characters")
        if action.__len__() > 1024 or action.__len__() < 1:
            raise ValueError("You must provide actions with length between 1 and 1024 characters")

    def verify_url(self, url):
            validator = URLValidator()
            validator(url)
