__author__ = 'arobres'

import utils as Utils


def create_random_rule():
    rule = {
            "action": {
                "actionName": "notify-scale",
                "operation": "scaleDown"
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