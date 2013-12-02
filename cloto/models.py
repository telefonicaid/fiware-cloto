__author__ = 'Geon'
import json
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

