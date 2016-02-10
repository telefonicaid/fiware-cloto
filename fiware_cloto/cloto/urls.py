#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
from django.conf.urls import patterns, url

from restCloto import ServerRulesView, GeneralView, \
    ServersGeneralView, ServerView, GeneralRulesView, GeneralRulesViewRule, ServerSubscriptionView, ServerRuleView
from fiware_cloto.cloto.views import info, fail

urlpatterns = patterns('',
    url(r'^info', info),
    url(r'^fail$', fail),
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
        url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/$', ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/(?P<subscriptionId>[-\w]+)/$',
        ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription/(?P<subscriptionId>[-\w]+)',
        ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)/subscription', ServerSubscriptionView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers/(?P<serverId>[-\w]+)', ServerView()),
    url(r'^v1.0/(?P<tenantId>[-\w]+)/servers', ServersGeneralView()),

    url(r'^v1.0/(?P<tenantId>[-\w]+)', GeneralView())
)
