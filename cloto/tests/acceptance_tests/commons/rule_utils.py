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
                    "operand": "less equal",
                    "value": "1"
            },
                "cpu": {
                    "operand": "less",
                    "value": "1"
                    }
                }
            }
    return rule


def create_random_notify_rule():
    rule = {"action": {"actionName": "notify-email",
                       "body": "Be careful, the mem is too low!!!!",
                       "email": "aaa@aaa.es"
                       },
            "name": Utils.id_generator(),
            "condition": {
                "mem": {
                    "operand": "less equal",
                    "value": "1"
                },
                "cpu": {
                    "operand": "less",
                    "value": "1"
                }
            }
            }
    return rule

def create_scale_specific_rule(operation, name, mem_value, mem_operand, cpu_value, cpu_operand):

    if name == 'random':
        name = Utils.id_generator()

    rule = {
            "action": {
                "actionName": "notify-scale",
                "operation": operation
            },
            "name": name,
            "condition": {
                "mem": {
                    "operand": mem_operand,
                    "value": mem_value
            },
                "cpu": {
                    "operand": cpu_operand,
                    "value": cpu_value
                    }
                }
            }
    return rule

def create_notify_specific_rule(body, email, name, mem_value, mem_operand, cpu_value, cpu_operand):

    if name == 'random':
        name = Utils.id_generator()

    rule = {
            "action": {
                "actionName": "notify-email",
                "body": body,
                "email": email
            },
            "name": name,
            "condition": {
                "mem": {
                    "operand": mem_operand,
                    "value": mem_value
            },
                "cpu": {
                    "operand": cpu_operand,
                    "value": cpu_value
                    }
                }
            }
    return rule

