__author__ = 'gjp'
from django.db import models


class ServerInfo(models.Model):
    """This class models information about Cloto Server.
    """
    id = models.IntegerField(primary_key=True, max_length=1)
    owner = models.CharField(max_length=30)
    version = models.FloatField()
    runningfrom = models.DateTimeField()
    doc = models.CharField(max_length=100)


class SpecificRule(models.Model):
    """This class models information about specific rules for Virtual Machines deployed.
    """
    specificRule_Id = models.CharField(primary_key=True, max_length=30)
    tenantId = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    condition = models.CharField(max_length=30000)
    action = models.CharField(max_length=30000)
    createdAt = models.DateTimeField()


class Subscription(models.Model):
    """This class models the server subscription to a rule .
    """
    subscription_Id = models.CharField(primary_key=True, max_length=30)
    url = models.CharField(max_length=140)
    ruleId = models.CharField(max_length=30)
    serverId = models.CharField(max_length=30)
    cbSubscriptionId = models.CharField(max_length=30)


class Entity(models.Model):
    """This class models information about Virtual Machines deployed.
    """
    serverId = models.CharField(primary_key=True, max_length=30)
    tenantId = models.CharField(max_length=30)
    specificrules = models.ManyToManyField(SpecificRule, verbose_name="list of rules")
    subscription = models.ManyToManyField(Subscription, verbose_name="list of subscription")


class TenantInfo(models.Model):
    """This class models information about tenants and their windowsize.
    """
    tenantId = models.CharField(primary_key=True, max_length=30)
    windowsize = models.IntegerField()


class Rule(models.Model):
    """This class models information about general rules.
    """
    ruleId = models.CharField(primary_key=True, max_length=30)
    tenantId = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    condition = models.CharField(max_length=30000)
    action = models.CharField(max_length=30000)
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
