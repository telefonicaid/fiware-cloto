__author__ = 'Geon'
import json
import requests
from configuration import CONTEXT_BROKER_URL, NOTIFICATION_URL, NOTIFICATION_TIME, NOTIFICATION_TYPE
import constants
from cloto.log import logger


class OrionClient():
    """This class provides methods to provide connection with Orion Context Broker.
    """
    client = requests

    def contextBrokerSubscription(self, tenantId, serverId):
        """Subscribes server to Context Broker to get information about cpu and memory monitoring"""

        headers = {constants.CONTENT_HEADER: constants.JSON_TYPE, constants.ACCEPT_HEADER: constants.JSON_TYPE}

        data = '{"entities": [' \
               '{"type": "Server",'\
               '"isPattern": "false",' \
                          '"id": "' + serverId + '"' \
                          '}],' \
                '"attributes": [' \
                            '"cpu",' \
                            '"mem"],' \
                            '"reference": "' + NOTIFICATION_URL + '/' + tenantId + 'servers/' + serverId + '",' \
                            '"duration": "P1M",' \
                            '"notifyConditions": [' \
                            '{"type": "' + NOTIFICATION_TYPE + '",' \
                            '"condValues": ["' + NOTIFICATION_TIME + '"]}]}'

        r = self.client.post(CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)

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

        r = self.client.post(CONTEXT_BROKER_URL + "/unsubscribeContext", data, headers=headers)
        if r.status_code == 200:
            logger.info("Server %s was unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        else:
            logger.error("ERROR, Server %s was not unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
