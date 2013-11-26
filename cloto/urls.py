from django.conf.urls import patterns, url
from cloto import views
from restCloto import ServerRulesView, GeneralView, ServersGeneralView, ServerView


urlpatterns = patterns('',
    url(r'^v1.0/(?P<tenantId>\w+)/servers/$', ServersGeneralView()),
    url(r'^v1.0/(?P<tenantId>\w+)/servers/(?P<serverId>\w+)/$', ServerView()),
    url(r'^v1.0/(?P<tenantId>\w+)/servers/(?P<serverId>\w+)/rules/$', ServerRulesView()),
    url(r'^v1.0/(?P<tenantId>\w+)/servers/(?P<serverId>\w+)/rules/(?P<ruleId>\w+)/$', ServerRulesView()),
    url(r'^v1.0/(?P<tenantId>\w+)/$', GeneralView()),
    url(r'^v1.0/(?P<tenantId>\w+)/rules/$', GeneralView()),
)
