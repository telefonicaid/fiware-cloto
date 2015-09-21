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
import datetime
import json
import uuid

import yaml
from fiware_cloto.orion_wrapper import orion_client as orion_client
from fiware_cloto.cloto.utils.log import logger
from django.utils import timezone
from django.core.validators import URLValidator, validate_email
from keystoneclient.exceptions import Conflict
from fiware_cloto.cloto.constants import OPERATIONS, OPERANDS
from fiware_cloto.cloto.models import Rule, RuleModel, ListRuleModel, Entity, SpecificRule, \
    Subscription, SubscriptionModel


class RuleManager():
    """This class provides methods to manage rules.
    """
    #ContextBrokerClient
    orionClient = orion_client.orion_client()

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
        """Splits condition from a rule.

        :param str rule:        The rule description in json format
        """
        condition = yaml.load(rule)['condition']
        return condition

    def getAction(self, rule):
        """Splits action from a rule.

        :param str rule:        The rule description in json format
        """
        action = yaml.load(rule)['action']
        return action

    def getName(self, rule):
        """Splits the name from a rule.

        :param str rule:        The rule description in json format
        """
        name = yaml.load(rule)['name']
        return name

    def create_specific_rule(self, tenantId, serverId, rule):
        """Creates a new specific rule for a server

        :param str tenantId:    The id of the tenant
        :param str serverId:    The id of the server
        :param str rule:        The rule description in json format
        """
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

        #Its necesary modify action to get subscriptionId
        modifiedAction = self.pimp_rule_action(action, name, serverId)
        modifiedCondition = self.pimp_rule_condition(condition, name, serverId)

        createdAt = datetime.datetime.now(tz=timezone.get_default_timezone())
        ruleId = uuid.uuid1()
        rule = SpecificRule(specificRule_Id=ruleId,
                tenantId=tenantId, name=name, condition=condition, action=action,
                clips_condition=modifiedCondition, clips_action=modifiedAction, createdAt=createdAt)
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
        logger.info("RuleId %s was created for server %s" % (str(ruleId), serverId))
        return ruleResult

    def update_specific_rule(self, tenantId, serverId, ruleId, rule):
        """Updates a specific rule

        :param str tenantId:    The id of the tenant
        :param str serverId:    The id of the server
        :param str ruleId:      The id of the rule
        :param str rule:        The rule description in json format
        """

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
        modifiedAction = self.pimp_rule_action(action, name, serverId)
        modifiedCondition = self.pimp_rule_condition(condition, name, serverId)
        rule_db.clips_action = modifiedAction
        rule_db.clips_condition = modifiedCondition
        rule_db.save()
        ruleResult = RuleModel()
        ruleResult.ruleId = str(ruleId)
        ruleResult.name = name
        ruleResult.condition = condition
        ruleResult.action = action
        logger.info("RuleId %s was updated" % str(ruleId))
        return ruleResult

    def get_specific_rule(self, tenantId, serverId, ruleId):
        """Returns information about a specific rule.

        :param str tenantId:    The id of the tenant
        :param str serverId:    The id of the server
        :param str ruleId:      The id of the rule
        """
        r_query = SpecificRule.objects.get(specificRule_Id__exact=ruleId,
                                           tenantId__exact=tenantId, entity__exact=serverId)
        rule = RuleModel()
        rule.ruleId = r_query.__getattribute__("specificRule_Id")
        rule.name = r_query.__getattribute__("name")
        rule.condition = r_query.__getattribute__("condition")
        rule.action = r_query.__getattribute__("action")
        return rule

    def get_all_specific_rules(self, tenantId, serverId):
        """Returns all specific rules of a server.

        :param str tenantId:    The id of the tenant
        :param str serverId:    The id of the server
        """
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
        """Deletes a specific rule.

        :param str tenantId:    The id of the tenant
        :param str serverId:    The id of the server
        :param str ruleId:      The id of the rule
        """
        r_query = SpecificRule.objects.get(specificRule_Id__exact=ruleId,
                                           tenantId__exact=tenantId, entity__exact=serverId)
        r_query.delete()

        #Deleting subscriptions to that rule
        subscriptions = Subscription.objects.filter(ruleId__exact=ruleId)
        subscriptions.delete()
        logger.info("RuleId %s from server %s was deleted" % (ruleId, serverId))
        return True

    def get_all_entities(self, tenantId):
        """Returns all servers with their information.

        :param str tenantId:      The id of the tenant
        """

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
        """Creates a server subscription to a rule.

        :param str tenantId:        The id of the tenant
        :param str serverId:        The id of the server
        :param str subscription:    The subscription description in json format
        """
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
                context_broker_subscription = sub.cbSubscriptionId
            if sub.ruleId == ruleId:
                raise Conflict("Subscription already exists")

        self.verify_url(url)
        if not context_broker_subscription:
            cbSubscriptionId = self.orionClient.contextBrokerSubscription(tenantId, serverId)
        else:
            cbSubscriptionId = context_broker_subscription
        subscription_Id = uuid.uuid1()
        subscr = Subscription(subscription_Id=subscription_Id, ruleId=ruleId, url=url, serverId=serverId,
                              cbSubscriptionId=cbSubscriptionId)
        subscr.save()
        entity.subscription.add(subscr)
        entity.save()
        logger.info("Server %s was subscribed to rule %s: cbSubscriptionId is %s and internal subscription %s"
                        % (serverId, ruleId, cbSubscriptionId, str(subscription_Id)))

        return subscription_Id

    def unsubscribe_to_rule(self, serverId, subscriptionId):
        """Unsuscribe a server from a rule.

        :param str tenantId:        The id of the tenant
        :param str serverId:        The id of the server
        :param str subscriptionId:  The id of the subscription
        """

        r_query = Subscription.objects.get(subscription_Id__exact=subscriptionId, serverId__exact=serverId)
        if Subscription.objects.filter(serverId__exact=serverId).count() == 1:
            self.orionClient.contextBrokerUnSubscription(r_query.cbSubscriptionId, r_query.serverId)
            r_query.delete()
        else:
            r_query.delete()
        logger.info("Server %s was unsubscribed to this subscription: %s"
                        % (serverId, subscriptionId))
        return True

    def get_subscription(self, tenantId, serverId, subscriptionId):
        """Returns information about a subscription.

        :param str tenantId:        The id of the tenant
        :param str serverId:        The id of the server
        :param str subscriptionId:  The id of the subscription
        """

        r_query = Subscription.objects.get(subscription_Id__exact=subscriptionId, serverId__exact=serverId)
        subscription = SubscriptionModel()
        subscription.ruleId = r_query.__getattribute__("ruleId")
        subscription.serverId = r_query.__getattribute__("serverId")
        subscription.url = r_query.__getattribute__("url")
        subscription.subscriptionId = r_query.__getattribute__("subscription_Id")
        return subscription

    def checkRule(self, name, condition, action):
        """Checks if the parts of the rule fulfill the expected character limit

        :param str name:        The name of the rule
        :param str condition:   The description of the condition
        :param str action:      The description of the actions
        """

        try:
            if name.__len__() > 30 or name.__len__() < 3:
                raise ValueError("You must provide a name with length between 3 and 30 characters")
            if condition.__len__() > 1024 or condition.__len__() < 1:
                raise ValueError("You must provide conditions with length between 1 and 1024 characters")
            if action.__len__() > 1024 or action.__len__() < 1:
                raise ValueError("You must provide actions with length between 1 and 1024 characters")
        except ValueError as ex:
            raise ex

    def verify_url(self, url):
        """Checks if the string is valid URL

        :param str url:      The expected url
        """
        validator = URLValidator()
        validator(url)

    def verify_email(self, email):
        """Checks if the string is valid email

        :param str email:      The expected email
        """
        validate_email(email)

    def verify_values(self, name, value, type):
        """Checks if rule operands are expected strings and values are valid floats

        :param str name:        The name
        :param str value:       The value
        :param object type:     The type of the value
        """
        try:
            if value == None or value == "":
                raise ValueError()
            if type == str:
                if name == "operation" and value not in OPERATIONS:
                    raise ValueError
                if "operand" in name and (value not in OPERANDS):
                    raise ValueError
            else:
                if type == float:
                    myfloat = float(value)
                if myfloat < 0.0 or myfloat > 100.0:
                    raise ValueError
        except ValueError:
            raise ValueError("You must provide a valid value and operand for %s" % name)

    def pimp_rule_action(self, action, ruleName, serverId):
        """This method builds a CLIPS rule from data received as json.
        It is necesary to Rule Engine add this String to be able to get the notification url of each Rule subscribed

        :param str action:          The description of the action
        :param str ruleName:        The name of the rule
        :param object serverId:     The id of the server
        """
        try:
            actionName = action['actionName']
            self.verify_values('actionName', actionName, str)
            action_string = "(python-call " + actionName + " \"" + serverId + "\" ?url"

            if actionName == "notify-email":
                email = action['email']
                body = action['body']
                self.verify_email(email)
                self.verify_values("body", body, str)
                action_string += " \"" + body + "\"" " " + email
            if actionName == "notify-scale":
                operation = action['operation']
                self.verify_values("operation", operation, str)
                action_string += " \"" + operation + "\""
            action_string += ")"
            string_to_get_url_subscription = "(bind ?url (python-call get-notification-url \"" + ruleName\
                                             + "\" \"" + serverId + "\"))"
            return string_to_get_url_subscription + action_string
        except ValueError as error:
            raise error
        except KeyError as error:
            raise error

    def pimp_rule_condition(self, condition, ruleName, serverId):
        """This method builds a CLIPS condition from data received as json.

        :param str condition:       The description of the condition
        :param str ruleName:        The name of the rule
        :param object serverId:     The id of the server
        """

        try:
            operands = {"less": "<", "greater": ">", "less equal": "<=", "greater equal": ">="}
            condition_string = "(ServerFact \"" + serverId + "\""

            ##Adding CPU condition
            parameters = ["cpu", "mem", "hdd", "net"]
            for k in parameters:
                self.verify_values(k + " operand", condition[k]["operand"], str)
                self.verify_values(k, condition[k]["value"], float)
                operand = operands[condition[k]["operand"]]
                condition_string += " ?" + k + "&:(" + operand + " ?" + k + " " \
                                    + str(condition[k]["value"]) + ")"
            condition_string += ")"
            return condition_string
        except ValueError as error:
            raise error
        except KeyError as error:
            raise error
