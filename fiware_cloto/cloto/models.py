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
from django.db import models

from fiware_cloto.cloto.constants import DOC_LENGTH, ID_LENGTH, NAME_LENGTH, TEXT_LENGTH, URL_LENGTH, VERSION_LENGTH


class ServerInfo(models.Model):
    """This class models information about Cloto Server.
    """
    id = models.IntegerField(primary_key=True)
    owner = models.CharField(max_length=NAME_LENGTH)
    version = models.CharField(max_length=VERSION_LENGTH)
    runningfrom = models.DateTimeField()
    doc = models.CharField(max_length=DOC_LENGTH)


class SpecificRule(models.Model):
    """This class models information about specific rules for Virtual Machines deployed.
    """
    specificRule_Id = models.CharField(primary_key=True, max_length=ID_LENGTH)
    tenantId = models.CharField(max_length=ID_LENGTH)
    name = models.CharField(max_length=NAME_LENGTH)
    condition = models.TextField(max_length=TEXT_LENGTH)
    action = models.TextField(max_length=TEXT_LENGTH)
    clips_condition = models.TextField(max_length=TEXT_LENGTH)
    clips_action = models.TextField(max_length=TEXT_LENGTH)
    createdAt = models.DateTimeField()


class Subscription(models.Model):
    """This class models the server subscription to a rule .
    """
    subscription_Id = models.CharField(primary_key=True, max_length=ID_LENGTH)
    url = models.CharField(max_length=URL_LENGTH)
    ruleId = models.CharField(max_length=ID_LENGTH)
    serverId = models.CharField(max_length=ID_LENGTH)
    cbSubscriptionId = models.CharField(max_length=ID_LENGTH)


class Entity(models.Model):
    """This class models information about Virtual Machines deployed.
    """
    serverId = models.CharField(primary_key=True, max_length=ID_LENGTH)
    tenantId = models.CharField(max_length=ID_LENGTH)
    specificrules = models.ManyToManyField(SpecificRule, verbose_name="list of rules")
    subscription = models.ManyToManyField(Subscription, verbose_name="list of subscription")


class TenantInfo(models.Model):
    """This class models information about tenants and their windowsize.
    """
    tenantId = models.CharField(primary_key=True, max_length=ID_LENGTH)
    windowsize = models.IntegerField()


class Rule(models.Model):
    """This class models information about general rules.
    """
    ruleId = models.CharField(primary_key=True, max_length=ID_LENGTH)
    tenantId = models.CharField(max_length=ID_LENGTH)
    name = models.CharField(max_length=ID_LENGTH)
    condition = models.TextField(max_length=TEXT_LENGTH)
    action = models.TextField(max_length=TEXT_LENGTH)
    createdAt = models.DateTimeField()


class SubscriptionModel():

    """This class contains information about subscriptions in order to serialize it and work with.
    """
    subscriptionId = None
    ruleId = None
    serverId = None
    url = None


class RuleModel():

    """This class contains information about general rules in order to serialize it and work with.
    """
    ruleId = None
    tenantId = None
    name = None
    condition = None
    action = None
    createdAt = None


class ListRuleModel():
    """This class contains information about lists of general rules in order to serialize it and work with.
    """
    tenantId = None
    rules = None
    serverId = None
    servers = None
    subscription = None


class TokenModel():
    """
    Define a Token model (not stored in DB).
    """
    username = None
    tenant = None
    id = None
    expires = None

    def __init__(self, username, id, expires, tenant=None):
        self.username = username
        self.id = id
        self.expires = expires
        self.tenant = tenant
