from django.conf.urls import patterns, url
from cloto import views
from restCloto import ServerRulesView, GeneralView, \
    ServersGeneralView, ServerView, GeneralRulesView, GeneralRulesViewRule, ServerSubscriptionView, ServerRuleView


urlpatterns = patterns('',
    url(r'^v1.0/(?P<tenantId>[-\w]+)/$', GeneralView()),

    url(r'^v1.0/(?P<tenantId>[-\w]+)/rules/$', GeneralRulesView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/rules/(?P<ruleId>[-\w]+)', GeneralRulesViewRule()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/rules', GeneralRulesView()),

    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/$', ServersGeneralView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/$', ServerView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/rules/$', ServerRulesView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/rules/(?P<ruleId>[-\w]+)/$', ServerRuleView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/rules/(?P<ruleId>[-\w]+)', ServerRuleView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/rules', ServerRulesView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)', ServerView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers', ServersGeneralView()),


    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/$', ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/(?P<subscriptionId>[-\w]+)/$',
        ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/(?P<subscriptionId>[-\w]+)',
        ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription', ServerSubscriptionView()),

    url(r'^v1.0/(?P<tenantId>[-\w]+)', GeneralView())
)
