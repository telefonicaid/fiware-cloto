__author__ = 'arobres'

import utils as Utils
import random
from constants import RULE_ACTION_SCALE_LIST


def create_random_scalability_rule():
    rule = {
            "action": {
                "actionName": "notify-scale",
                "operation": random.choice(RULE_ACTION_SCALE_LIST)
            },
            "name": Utils.id_generator(),
            "condition": {
                "mem": {
                    "operation": "less equal",
                    "value": "1"
            },
                "cpu": {
                    "operation": "less",
                    "value": "1"
                    }
                }
            }
    return rule


def create_random_notify_rule():
    rule = {"action": {"actionName": "notify-scale",
                       "description": "Be careful, the mem is too low!!!!",
                       "email": "aaa@aaa.es"
                       },
            "name": Utils.id_generator(),
            "condition": {
                "mem": {
                    "operation": "less equal",
                    "value": "1"
                },
                "cpu": {
                    "operation": "less",
                    "value": "1"
                }
            }
            }
    return rule