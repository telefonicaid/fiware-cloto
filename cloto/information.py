__author__ = 'gjp'
import json
from models import tenantInfo, serverInfo


class information():

    def __init__(self, tenantId=None, owner=None, windowsize=None, version=None, runningfrom=None, doc=None):
        if tenantId:
            self.startingParameters(tenantId)
        else:
            self.owner = owner
            self.windowsize = windowsize
            self.version = version
            self.runningfrom = runningfrom.strftime("%y/%m/%d %H:%M:%S")
            self.doc = doc

    def parse(self, d):
        """
        Convert from a dict to an information object.
        """
        try:
            self.windowsize = json.loads(d)['windowsize']
            return self
        except (ValueError, KeyError, TypeError):
            print ("error")
            return None

    def updateWindowSize(self, tenantId, newSize):
        t = tenantInfo.objects.get(tenantId__exact=tenantId)
        t.windowsize = newSize
        t.save()

    def startingParameters(self, tenantId):
        s = serverInfo.objects.get(id__exact='1')
        t = tenantInfo.objects.get(tenantId__exact=tenantId)
        self.owner = s.__getattribute__("owner")
        self.windowsize = t.__getattribute__("windowsize")
        self.version = s.__getattribute__("version")
        self.runningfrom = s.__getattribute__("runningfrom").strftime("%y/%m/%d %H:%M:%S")
        self.doc = s.__getattribute__("doc")

    def getVars(self):
        return vars(self)
