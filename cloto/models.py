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


class Entity(models.Model):
    """This class models information about Virtual Machines deployed.
    """
    entity_Id = models.CharField(primary_key=True, max_length=30)
    tenantId = models.CharField(max_length=30)
    specificrules = models.ManyToManyField(SpecificRule, verbose_name="list of rules")


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


class RuleModel():
    """This class contains information about general rules in order to serialize it and work with.
    """
    ruleId = None
    tenantId = None
    name = None
    condition = None
    action = None
    createdAt = None

    def getVars(self):
        return vars(self)


class ListRuleModel():
    """This class contains information about lists of general rules in order to serialize it and work with.
    """
    tenantId = None
    rules = None

    def getVars(self):
        return vars(self)
