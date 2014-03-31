__author__ = 'Geon'
import json
import requests
from configuration import CONTEXT_BROKER_URL, NOTIFICATION_URL, LOGGING_PATH
import logging
logger = logging.getLogger('RuleEngine')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGGING_PATH + '/RuleEngine.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s policymanager.cloto [-] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class OrionClient():
    """This class provides methods to provide connection with Orion Context Broker.
    """
    client = requests

    def contextBrokerSubscription(self, tenantId, serverId):
        """Subscribes server to Context Broker to get information about cpu and memory monitoring"""
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps("{\"entities\": ["
                          "{\"type\": \"Server\","
                          "\"isPattern\": \"false\","
                          "\"id\": \"%s\""
                          "}],"
                          "\"attributes\": ["
                            "\"cpu\","
                            "\"mem\"],"
                            "\"reference\": \"%s\","
                            "\"duration\": \"P1M\","
                            "\"notifyConditions\": ["
                            "{\"type\": \"ONTIMEINTERVAL\","
                            "\"condValues\": [\"PT5S\"]}]}" % (serverId,
                                                    NOTIFICATION_URL + "/" + tenantId + "servers/" + serverId))

        r = self.client.post(CONTEXT_BROKER_URL + "/subscribeContext", data, headers=headers)
        if r.status_code == 200:
            logger.info("[+] Server %s was subscribed to Context Broker.--- HTTP Response: %d" % (serverId, r.status_code))
        else:
            logger.error("[+] ERROR, Server %s was not subscribed to Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        decoded = json.loads(r.text.decode())
        return decoded["subscribeResponse"]["subscriptionId"]

    def contextBrokerUnSubscription(self, cbSubscriptionId, serverId):
        """Unsubscribes server from Context Broker """
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps("{\"subscriptionId\": \"%s\"}" % cbSubscriptionId)

        r = self.client.post(CONTEXT_BROKER_URL + "/unsubscribeContext", data, headers=headers)
        if r.status_code == 200:
            logger.info("[+] Server %s was unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        else:
            logger.error("[+] ERROR, Server %s was not unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
