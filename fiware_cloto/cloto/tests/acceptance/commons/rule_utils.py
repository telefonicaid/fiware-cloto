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

import random

from nose.tools import assert_equals, assert_true

from commons.configuration import TENANT_ID, HEADERS
from commons.errors import HTTP_CODE_NOT_OK
import utils as Utils
from commons.constants import RULE_ACTION_SCALE_LIST, DEFAULT_BODY, \
    RANDOM, RULE_ACTION, RULE_ACTION_NAME, BODY, \
    RULE_ACTION_NAME_LIST, MEM, CPU, EMAIL, RULE_NAME, RULE_CONDITION, RULE_OPERATION, RULE_OPERAND, RULE_VALUE, \
    RULE_ID, RULE_SPECIFIC_ID, HDD, NET


def create_scale_specific_rule(operation=random.choice(RULE_ACTION_SCALE_LIST), name=Utils.id_generator(),
                               mem_value=1, mem_operand='less equal', cpu_value=0, cpu_operand='less',
                               hdd_value=0, hdd_operand='less', net_value=0, net_operand='less'):

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

                },
                HDD: {
                    RULE_OPERAND: hdd_operand,
                    RULE_VALUE: hdd_value
                },
                NET: {
                    RULE_OPERAND: net_operand,
                    RULE_VALUE: net_value
                }
            }

    }

    return rule


def create_notify_specific_rule(body=DEFAULT_BODY, email="aaa@aaa.es", name=Utils.id_generator(), mem_value=1,
                                mem_operand='less equal', cpu_value=0, cpu_operand='less', hdd_value=0,
                                hdd_operand='less', net_value=0, net_operand='less'):

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
                    },
                HDD: {
                    RULE_OPERAND: hdd_operand,
                    RULE_VALUE: hdd_value
                },
                NET: {
                    RULE_OPERAND: net_operand,
                    RULE_VALUE: net_value
                }
            }

            }
    return rule


def assert_rule_information(response, rule_id=None, name=None, action=None, cpu=None, mem=None, hdd=None, net=None,
                            body=None):

    """Method to verify the rule body parameters
    :param response: Response body received from server
    :param rule_id: The expected rule identification number
    :param name: The expected rule name
    """
    if body is None:
        assert_equals(response[RULE_NAME], name)
        assert_equals(response[RULE_ID], rule_id)
        assert_equals(response[RULE_ACTION], action)
        assert_equals(response[RULE_CONDITION][CPU], cpu)
        assert_equals(response[RULE_CONDITION][MEM], mem)
        assert_equals(response[RULE_CONDITION][HDD], hdd)
        assert_equals(response[RULE_CONDITION][NET], net)
    else:
        assert_equals(response[RULE_NAME], body[RULE_NAME])
        assert_equals(response[RULE_ID], rule_id)


def create_rule_body(action=None, rule_id=None, condition=None, name=None):

    """Method to build the Rule JSON including rule_is

    :param rule_id: The expected rule identification number
    :param name: The expected rule name
    :param condition: The expected rule condition
    :param action: The expected rule action
    :returns: rule JSON (dict)
    """

    rule_body = {RULE_ACTION: action,
                 RULE_SPECIFIC_ID: rule_id,
                 RULE_CONDITION: condition,
                 RULE_NAME: name
                 }

    if action is None:
        del rule_body[RULE_ACTION]
    if rule_id is None:
        del rule_body[RULE_ID]
    if condition is None:
        del rule_body[RULE_CONDITION]
    if name is None:
        del rule_body[RULE_NAME]

    return rule_body


def create_rule(api_utils, tenant_id=TENANT_ID, server_id=None, rule_body=None, headers=HEADERS):

    """Method to subscribe a server to a specific rule not created.
    :param server_id: Server unique identifier
    :param headers: HTTP headers for the requests including authentication
    :param tenant_id: Tenant unique identifier
    :returns subscription_id: Subscription unique identifier
    """

    #Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=tenant_id, server_id=server_id, body=rule_body, headers=headers)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code))

    rule_id = req.json()[RULE_ID]
    return rule_id


def create_rule_parameter_dict(value=None, operand=None):

    """
    Method to create the parameter body for Create or Update rule dinamically
    :param value: Value of the parameter
    :param operand: Operand of the parameter
    :returns parameter body (dict)
    """
    tmp_dict = {}

    if value is not None:
        tmp_dict[RULE_VALUE] = value

    if operand is not None:
        tmp_dict[RULE_OPERAND] = operand

    return tmp_dict


def create_rule_action_dict(action_name=None, operation=None, body=None, email=None):

    """
    Method to create a rule action dict for scale or notify requests
    :param action_name: Name of the action to be executed when the rule is activated
    :param operation: Name of operation in the scale actions
    :param body: Message to be sent to notify the rule is activated
    :param body: email address to notify the rule is activated
    : returns Action body (dict)
    """

    action = {}

    if action_name is not None:
        action[RULE_ACTION_NAME] = action_name

    if operation is not None:
        action[RULE_OPERATION] = operation

    if body is not None:
        action[BODY] = body

    if email is not None:
        action[EMAIL] = email

    return action
