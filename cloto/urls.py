from django.conf.urls import patterns, url
from cloto import views
from restCloto import ServersView, GeneralView



urlpatterns = patterns('',
    url(r'^v1.0/?P<tenantIdd>/servers/(?P<serverId>\w+)/$', ServersView()),
    url(r'^v1.0/(?P<tenantId>\w+)/$', GeneralView()),
)
