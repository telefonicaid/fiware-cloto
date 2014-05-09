__author__ = 'gjp'
import cloto.information as information
from cloto.models import TenantInfo, ServerInfo
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from cloto.configuration import MAX_WINDOW_SIZE
from cloto.log import logger


class InfoManager():
    """This class provides methods to manage information about the server and windowsize of tenants.
    """

    def __init__(self):
        self.tenantInfo = self.get_tenant_information()
        self.serverInfo = self.get_server_information()

    def get_server_information(self):
        """Returns model of Information about server."""
        return ServerInfo

    def get_tenant_information(self):
        """Returns model of Information about a tenant."""
        return TenantInfo

    def get_information(self, tenantId):
        """Returns information about the server and tenant's windowsize."""
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
        """Updates windowsize of a specified tenant."""
        self.checkSize(newSize)
        t = self.tenantInfo.objects.get(tenantId__exact=tenantId)
        t.windowsize = newSize
        t.save()
        logger.info("%s windowsize updated to %d" % (tenantId, newSize))
        return t

    def setInformations(self, sInfo, tInfo):
        """Sets server information and tenant information to the InfoManager."""
        self.tenantInfo = tInfo
        self.serverInfo = sInfo

    def checkSize(self, newSize):
            if newSize <= 0 or newSize > MAX_WINDOW_SIZE:
                raise ValidationError("New size is not an integer between 1 and %d" % MAX_WINDOW_SIZE)
