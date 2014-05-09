__author__ = 'gjp'
from django.test import TestCase
from cloto.models import *
from cloto.manager import InfoManager
from mockito import *
from django.utils import timezone
import datetime


class InfoManagerTests(TestCase):
    def setUp(self):
        self.info = InfoManager.InfoManager()
        self.tenantId = "tenantId"
        self.originalSize = 5
        self.newSize = 4
        self.tenantInfoMocked = mock()
        self.serverInfoMocked = mock()
        mockedQuery = TenantInfo.objects.create(tenantId=self.tenantId, windowsize=self.originalSize)
        when(self.tenantInfoMocked).get(tenantId__exact=self.tenantId).thenReturn(mockedQuery)
        when(self.tenantInfoMocked).obects().thenReturn(self.tenantInfoMocked)
        serverQuery = ServerInfo.objects.create(id=1, owner="Telefonica I+D", version=1.0,
            runningfrom=datetime.datetime.now(tz=timezone.get_default_timezone()), doc="test")

    def test_get_server_information_model(self):
        s_model = self.info.get_server_information()
        self.assertEqual(ServerInfo, s_model)

    def test_get_tenant_information_model(self):
        t_model = self.info.get_tenant_information()
        self.assertEqual(TenantInfo, t_model)
