__author__ = 'arobres'

import utils as Utils
import random
from constants import RULE_ACTION_SCALE_LIST, DEFAULT_BODY

def create_scale_specific_rule(operation=random.choice(RULE_ACTION_SCALE_LIST), name=Utils.id_generator(), mem_value='1',
                               mem_operand='less equal', cpu_value='0', cpu_operand='less'):

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


def create_notify_specific_rule(body=DEFAULT_BODY, email="aaa@aaa.es", name=Utils.id_generator(), mem_value='1',
                                mem_operand='less equal', cpu_value='0', cpu_operand='less'):

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

