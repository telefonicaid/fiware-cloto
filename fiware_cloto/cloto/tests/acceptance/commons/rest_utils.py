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
__author__ = 'arobres'

from json import JSONEncoder

import requests

from commons.configuration import POLICY_MANAGER_PORT, POLICY_MANAGER_IP, HEADERS, FACTS_IP, FACTS_PORT
from commons.constants import RULE_ACTION, RULE_NAME, RULE_ID, RULE_URL, TENANT_WSIZE, CPU, MEM, HDD, NET,\
    RULE_CONDITION


POLICY_MANAGER_SERVER = 'http://{}:{}/v1.0'.format(POLICY_MANAGER_IP, POLICY_MANAGER_PORT)
FACTS_SERVER = 'http://{}:{}/v1.0'.format(FACTS_IP, FACTS_PORT)
UPDATE_CONTEXT_PATTERN = FACTS_SERVER + '/{tenant_id}/servers/{server_id}'
TENANT_PATTERN = '{url_root}/{tenant_id}/'
LIST_SERVERS_PATTERN = '{url_root}/{tenant_id}/servers'
SERVER_PATTERN = '{url_root}/{tenant_id}/servers/{server_id}'
CREATE_RULE_PATTERN = '{url_root}/{tenant_id}/servers/{server_id}/rules'
ELASTICITY_RULE_PATTERN = '{url_root}/{tenant_id}/servers/{server_id}/rules/{rule_id}'
CREATE_SUBSCRIPTION_PATTERN = '{url_root}/{tenant_id}/servers/{server_id}/subscription'
SUBSCRIPTION_PATTERN = '{url_root}/{tenant_id}/servers/{server_id}/subscription/{subscription_id}'


class RestUtils(object):

    def __init__(self):
        """Initialization method
        """

        self.api_url = POLICY_MANAGER_SERVER
        print "Initialized API REST Utils"

        self.encoder = JSONEncoder()

    def _call_api(self, pattern, method, body=None, headers=HEADERS, payload=None, **kwargs):

        """Launch HTTP request to Policy Manager API with given arguments
        :param pattern: string pattern of API url with keyword arguments (format string syntax)
        :param method: HTTP method to execute (string)
        :param body: JSON body content (dict)
        :param headers: HTTP header request (dict)
        :param payload: Query parameters for the URL
        :param **kwargs: URL parameters (without url_root) to fill the patters
        :returns: REST API response
        """

        kwargs['url_root'] = self.api_url

        url = pattern.format(**kwargs)
        print 'METHOD: {}\nURL: {} \nHEADERS: {} \nBODY: {}'.format(method, url, headers, self.encoder.encode(body))

        try:
            r = requests.request(method=method, url=url, data=self.encoder.encode(body), headers=headers,
                                 params=payload)
        except Exception, e:
            print "Request {} to {} crashed: {}".format(method, url, str(e))
            return None

        return r

    def retrieve_information(self, tenant_id, headers=HEADERS):

        """Retrieve the information of specific tenant
        :param tenant_id: Is the id of the tenant to obtain the information
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=TENANT_PATTERN, method='get', headers=headers, tenant_id=tenant_id)

    def update_window_size(self, tenant_id, window_size=None, headers=HEADERS):

        """Update the windows size in specific tenant
        :param tenant_id: Is the id of the tenant to obtain the information
        :param window_size: Number of measures probes required to check rules.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        json_body = {TENANT_WSIZE: window_size}

        return self._call_api(pattern=TENANT_PATTERN, method='put', headers=headers, body=json_body,
                              tenant_id=tenant_id)

    def retrieve_server_list(self, tenant_id=None, headers=HEADERS):

        """Retrieve a list with all servers and their rules.
        :param tenant_id: Is the id of the tenant to obtain the information
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=LIST_SERVERS_PATTERN, method='get', headers=headers, tenant_id=tenant_id)

    def retrieve_rules(self, tenant_id, server_id=None, headers=HEADERS):

        """Retrieve a list with all rules from specific server.
        :param tenant_id: Is the id of the tenant to obtain the information
        :param server_id: Is the id of the server to obtain the information
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """
        return self._call_api(pattern=SERVER_PATTERN, method='get', headers=headers, tenant_id=tenant_id,
                              server_id=server_id)

    def update_server_context(self, tenant_id, server_id, body=None, headers=HEADERS):

        return self._call_api(pattern=UPDATE_CONTEXT_PATTERN, method='post', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, body=body)

    def create_rule(self, tenant_id=None, server_id=None, rule_name=None, cpu=None, mem=None, hdd=None, net=None,
                        action=None, headers=HEADERS, body=None):

        """Create a new elasticity rule in specific server.
        :param tenant_id: Is the id of the tenant to obtain the information
        :param server_id: Is the id of the server to obtain the information
        :param rule_name: Key whose value represents the name of the rule.
        :param action: Is the action to take over the server when the rules are activated.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        if body is None:
            api_body = {}
            condition = {}
            if rule_name is not None:
                api_body[RULE_NAME] = rule_name

            if cpu is not None:
                condition[CPU] = cpu

            if mem is not None:
                condition[MEM] = mem

            if hdd is not None:
                condition[HDD] = hdd

            if net is not None:
                condition[NET] = net

            if len(condition) > 0:
                api_body[RULE_CONDITION] = condition

            if action is not None:
                api_body[RULE_ACTION] = action

        else:
            api_body = body

        return self._call_api(pattern=CREATE_RULE_PATTERN, method='post', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, body=api_body)

    def update_rule(self, tenant_id=None, server_id=None, rule_name=None, action=None, rule_id=None, cpu=None,
                    mem=None, hdd=None, net=None, body=None, headers=HEADERS):
        """Update a elasticity rule in specific server.
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param rule_name: Key whose value represents the name of the rule.
        :param condition: Is the description of the scalability rule associated to this server
        :param action: Is the action to take over the server when the rules are activated.
        :param rule_id: Is the id of the elasticity rule to be updated.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        if body is None:
            api_body = {}
            condition = {}
            if rule_name is not None:
                api_body[RULE_NAME] = rule_name

            if cpu is not None:
                condition[CPU] = cpu

            if mem is not None:
                condition[MEM] = mem

            if hdd is not None:
                condition[HDD] = hdd

            if net is not None:
                condition[NET] = net

            if len(condition) > 0:
                api_body[RULE_CONDITION] = condition

            if action is not None:
                api_body[RULE_ACTION] = action

        else:
            api_body = body

        return self._call_api(pattern=ELASTICITY_RULE_PATTERN, method='put', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, rule_id=rule_id, body=api_body)

    def delete_rule(self, tenant_id=None, server_id=None, rule_id=None, headers=HEADERS):
        """Delete a elasticity rule in specific server.
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param rule_id: Is the id of the elasticity rule to be deleted.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=ELASTICITY_RULE_PATTERN, method='delete', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, rule_id=rule_id)

    def retrieve_rule(self, tenant_id=None, server_id=None, rule_id=None, headers=HEADERS):

        """Retrieve a elasticity rule information in specific server.
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param rule_id: Is the id of the elasticity rule.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=ELASTICITY_RULE_PATTERN, method='get', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, rule_id=rule_id)

    def create_subscription(self, tenant_id=None, server_id=None, rule_id=None, url=None, headers=HEADERS):

        """Create a new subscription rule associated to a rule
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param rule_id: Is the id of the elasticity rule to do the subscription.
        :param url: Is the url to notify the action when the rule is fired.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        api_body = {}
        if rule_id is not None:
            api_body[RULE_ID] = rule_id
        if url is not None:
            api_body[RULE_URL] = url

        return self._call_api(pattern=CREATE_SUBSCRIPTION_PATTERN, method='post', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, body=api_body)

    def delete_subscription(self, tenant_id=None, server_id=None, subscription_id=None, headers=HEADERS):

        """Delete a subscription rule associated to a rule
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param subscription_id: Is the id of the subscription rule to be deleted.
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=SUBSCRIPTION_PATTERN, method='delete', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, subscription_id=subscription_id)

    def retrieve_subscription(self, tenant_id=None, server_id=None, subscription_id=None, headers=HEADERS):

        """Retrieve a subscription rule associated to a rule
        :param tenant_id: Is the id of the tenant.
        :param server_id: Is the id of the server.
        :param subscription_id: Is the id of the subscription rule..
        :param headers: HTTP header request (dict)
        :returns: REST API response from Policy Manager
        """

        return self._call_api(pattern=SUBSCRIPTION_PATTERN, method='get', headers=headers, tenant_id=tenant_id,
                              server_id=server_id, subscription_id=subscription_id)
