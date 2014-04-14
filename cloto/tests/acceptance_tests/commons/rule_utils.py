__author__ = 'arobres'

import utils as Utils
import random
from constants import RULE_ACTION_SCALE_LIST, DEFAULT_BODY, RANDOM, RULE_ACTION, RULE_ACTION_NAME, BODY, \
    RULE_ACTION_NAME_LIST, MEM, CPU, EMAIL, RULE_NAME, RULE_CONDITION,RULE_OPERATION, RULE_OPERAND, RULE_VALUE


def create_scale_specific_rule(operation=random.choice(RULE_ACTION_SCALE_LIST), name=Utils.id_generator(),
                               mem_value='1', mem_operand='less equal', cpu_value='0', cpu_operand='less'):

    """Method to create a default scalability rule body used to create or update rules
    :param operation: operation to be performed by the Scalability manager
    :param name: Rule name
    :param cpu_value mem_value: value of the parameter to match
    :param cpu_operand mem_operand: operand of the parameter to match
    :returns json body (dict)
    """

    if name == RANDOM:
        name = Utils.id_generator()

    rule = {
            RULE_ACTION: {
                RULE_ACTION_NAME: RULE_ACTION_NAME_LIST[0],
                RULE_OPERATION: operation
            },
            RULE_NAME: name,
            RULE_CONDITION: {
                MEM: {
                    RULE_OPERAND: mem_operand,
                    RULE_VALUE: mem_value
            },
                CPU: {
                    RULE_OPERAND: cpu_operand,
                    RULE_VALUE: cpu_value
                    }
                }
            }

    return rule


def create_notify_specific_rule(body=DEFAULT_BODY, email="aaa@aaa.es", name=Utils.id_generator(), mem_value='1',
                                mem_operand='less equal', cpu_value='0', cpu_operand='less'):

    """Method to create a default notify rule body used to create or update rules
    :param body: body to be send to the user
    :param name: Rule name
    :param cpu_value mem_value: value of the parameter to match
    :param cpu_operand mem_operand: operand of the parameter to match
    :returns json body (dict)
    """

    if name == RANDOM:
        name = Utils.id_generator()

    rule = {
            RULE_ACTION: {
                RULE_ACTION_NAME: RULE_ACTION_NAME_LIST[1],
                BODY: body,
                EMAIL: email
            },
            RULE_NAME: name,
            RULE_CONDITION: {
                MEM: {
                    RULE_OPERAND: mem_operand,
                    RULE_VALUE: mem_value
            },
                CPU: {
                    RULE_OPERAND: cpu_operand,
                    RULE_VALUE: cpu_value
                    }
                }
            }
    return rule
