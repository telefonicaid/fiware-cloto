__author__ = 'Geon'
from django.db import models


class ServerInfo(models.Model):
    id = models.IntegerField(primary_key=True, max_length=1)
    owner = models.CharField(max_length=30)
    version = models.FloatField()
    runningfrom = models.DateTimeField()
    doc = models.CharField(max_length=100)


class TenantInfo(models.Model):
    tenantId = models.CharField(primary_key=True, max_length=30)
    windowsize = models.IntegerField()


class Rule(models.Model):
    ruleId = models.CharField(primary_key=True, max_length=30)
    tenantId = models.CharField(max_length=30)
    condition = models.CharField(max_length=30000)
    action = models.CharField(max_length=30000)
    createdAt = models.DateTimeField()


class RuleModel():
    ruleId = None
    tenantId = None
    condition = None
    action = None
    createdAt = None

    def getVars(self):
        return vars(self)


class ListRuleModel():
    tenantId = None
    rules = None

    def getVars(self):
        return vars(self)
