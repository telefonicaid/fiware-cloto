__author__ = 'gjp'
import cloto.information as information
from cloto.models import TenantInfo, ServerInfo


class InfoManager():

    def __init__(self):
        self.tenantInfo = self.get_tenant_information()
        self.serverInfo = self.get_server_information()

    def get_server_information(self):
        return ServerInfo

    def get_tenant_information(self):
        return TenantInfo

    def get_information(self, tenantId):
        serverInfo = self.get_server_information()
        tenantInfo = self.get_tenant_information()
        s_query = serverInfo.objects.get(id__exact='1')
        t_query = tenantInfo.objects.get(tenantId__exact=tenantId)
        owner = s_query.__getattribute__("owner")
        windowsize = t_query.__getattribute__("windowsize")
        version = s_query.__getattribute__("version")
        runningfrom = s_query.__getattribute__("runningfrom")
        doc = s_query.__getattribute__("doc")
        return information.information(owner, windowsize, version, runningfrom, doc)

    def updateWindowSize(self, tenantId, newSize):
        t = self.tenantInfo.objects.get(tenantId__exact=tenantId)
        t.windowsize = newSize
        t.save()

    def setInformations(self, sInfo, tInfo):
        self.tenantInfo = tInfo
        self.serverInfo = sInfo
