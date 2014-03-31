__author__ = 'Geon'
import json
import requests
from configuration import CONTEXT_BROKER_URL, NOTIFICATION_URL


class OrionClient():
    """This class provides methods to provide connection with Orion Context Broker.
    """
    client = requests

    def contextBrokerSubscription(self, tenantId, serverId):
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
            print("[+] Server %s was subscribed to Context Broker.--- HTTP Response: %d" % (serverId, r.status_code))
        else:
            print("[+] ERROR, Server %s was not subscribed to Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        decoded = json.loads(r.text.decode())
        return decoded["subscribeResponse"]["subscriptionId"]

    def contextBrokerUnSubscription(self, cbSubscriptionId, serverId):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps("{\"subscriptionId\": \"%s\"}" % cbSubscriptionId)

        r = self.client.post(CONTEXT_BROKER_URL + "/unsubscribeContext", data, headers=headers)
        if r.status_code == 200:
            print("[+] Server %s was unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
        else:
            print("[+] ERROR, Server %s was not unsubscribed from Context Broker.--- HTTP Response: %d"
                  % (serverId, r.status_code))
