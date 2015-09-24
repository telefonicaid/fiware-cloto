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
__author__ = 'gjp'
import json
import logging as logger

import requests
from django.conf import settings

from fiware_cloto.cloto.constants import CONTENT_HEADER, JSON_TYPE, ACCEPT_HEADER


class orion_client():
    """This class provides methods to provide connection with Orion Context Broker.
    """
    client = requests

    def contextBrokerSubscription(self, tenantId, serverId):
        """Subscribes server to Context Broker to get information about cpu and memory monitoring"""

        headers = {CONTENT_HEADER: JSON_TYPE, ACCEPT_HEADER: JSON_TYPE}

        data = '{"entities": [' \
               '{"type": "Server",'\
               '"isPattern": "false",' \
                          '"id": "' + serverId + '"' \
                          '}],' \
                '"attributes": [' \
                            '"cpu",' \
                            '"mem"],' \
                            '"reference": "' + settings.NOTIFICATION_URL + '/' + \
                            tenantId + 'servers/' + serverId + '",' \
                            '"duration": "P1M",' \
                            '"notifyConditions": [' \
                            '{"type": "' + settings.NOTIFICATION_TYPE + '",' \
                            '"condValues": ["' + settings.NOTIFICATION_TIME + '"]}]}'

        r = self.client.post(settings.CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)

        if r.status_code == 200:
            decoded = json.loads(r.text.decode())
            logger.info("Server %s was subscribed to Context Broker.--- HTTP Response: %d" % (serverId, r.status_code))

        else:
            logger.error("ERROR, Server %s was not subscribed to Context Broker.--- HTTP Response: %d"
                % (serverId, r.status_code))
            raise SystemError("ERROR, Server %s was not subscribed to Context Broker.--- HTTP Response: %d"
                % (serverId, r.status_code))

        return decoded["subscribeResponse"]["subscriptionId"]

    def contextBrokerUnSubscription(self, cbSubscriptionId, serverId):
        """Unsubscribes server from Context Broker """
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps("{\"subscriptionId\": \"%s\"}" % cbSubscriptionId)

        r = self.client.post(settings.CONTEXT_BROKER_URL + "/unsubscribeContext", data, headers=headers)
        if r.status_code == 200:
            logger.info("Server %s was unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        else:
            logger.error("ERROR, Server %s was not unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
            raise SystemError("ERROR, Server %s was not unsubscribed.--- HTTP Response: %d"
                % (serverId, r.status_code))
