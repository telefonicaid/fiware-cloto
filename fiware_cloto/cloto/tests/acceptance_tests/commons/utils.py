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

import string
import random

from nose.tools import assert_in, assert_equals

from constants import CONTENT_TYPE_HEADER, AUTHENTICATION_HEADER, DEFAULT_CONTENT_TYPE_HEADER, RULE_SPECIFIC_ID
from constants import ATTRIBUTES_NAME, ATTRIBUTES_TYPE, ATTRIBUTES_VALUE, ATTRIBUTES_LIST, ATTRIBUTE_PROBE, ATTRIBUTES
from constants import CONTEXT_IS_PATTERN, CONTEXT_IS_PATTERN_VALUE, CONTEXT_SERVER, \
    CONTEXT_SERVER_ID, CONTEXT_TYPE, CONTEXT_ELEMENT, SERVERS, RULES, SERVER_ID, RULE_URL_DEFAULT, RULE_ID
from constants import CONTEXT_STATUS_CODE_CODE, CONTEXT_STATUS_CODE_DETAILS, CONTEXT_STATUS_CODE_OK, \
    CONTEXT_STATUS_CODE_REASON, CONTEXT_STATUS_CODE, ORIGINATOR, CONTEXT_RESPONSES, SUBSCRIPTION_ID, RESPONSE_OK_CODE
from commons.errors import FAULT_ELEMENT_ERROR, ERROR_CODE_ERROR
from configuration import TENANT_ID, HEADERS
from rest_utils import RestUtils

list_deletions = [None, u'null']


def create_header(content_type=DEFAULT_CONTENT_TYPE_HEADER, token=None):

    """Method to create the header required to perform requests to the Policy Manager
    :param content_type:  Content type of the HTTP request. By default application/json
    :param token: Token required to policy manager authentication
    :returns: HTTP header (dict)
    """

    header = {CONTENT_TYPE_HEADER: '', AUTHENTICATION_HEADER: ''}

    if content_type in list_deletions:
        del header[CONTENT_TYPE_HEADER]
    else:
        header[CONTENT_TYPE_HEADER] = content_type

    if token in list_deletions:
        del header[AUTHENTICATION_HEADER]
    else:
        header[AUTHENTICATION_HEADER] = token

    return header


def assert_error_code_error(response, expected_error_code=None, expected_fault_element=None):

    """Method to assert response errors from Policy Manger
    :param response: Response obtained from thelett API REST request to the Policy Manager
    :param expected_fault_element: Expected Fault element in the JSON response
    :param expected_error_code: Expected Error code in the JSON response
    """

    assert_equals(expected_error_code, str(response.status_code),
                  ERROR_CODE_ERROR.format(expected_error_code, str(response.status_code)))
    response_body = response.json()
    assert_in(expected_fault_element, response_body.keys(),
              FAULT_ELEMENT_ERROR.format(expected_fault_element, response_body))
    assert_equals(str(response_body[expected_fault_element]['code']), expected_error_code,
                  ERROR_CODE_ERROR.format(expected_error_code, response_body[expected_fault_element]['code']))


def id_generator(size=10, chars=string.ascii_letters + string.digits):

    """Method to create random ids
    :param size: define the string size
    :param chars: the characters to be use to create the string
    return ''.join(random.choice(chars) for x in range(size))
    """

    return ''.join(random.choice(chars) for x in range(size))


def assert_json_format(request):

    """"Method to assert the JSON format
    :param request: Object with the response
    :return response if is JSON compliance
    """

    try:
        response = request.json()
    except ValueError:
        assert False, "JSON Cannot be decode. Response format not correspond with JSON format"

    return response


def context_element(cpu_value=None, memory_value=None, disk_value=None, network_value=None, server_id=None):

    """Method to create one context server body
    :param cpu_value: current value of the CPU
    :param memory_value: current value of the RAM memory
    :param disk_value: current value of the HDD
    :param network_value: current value of the network
    :param server_id: Server unique identifier
    :returns context_server_body:
    """

    context_attributes_body = []
    attribute_values = [cpu_value, memory_value, disk_value, network_value]
    for name, value in zip(ATTRIBUTES_LIST, attribute_values):

        if value is None:
            pass
        elif value == 'None':
            pass
        else:
            context_attributes_body.append({ATTRIBUTES_NAME: name, ATTRIBUTES_TYPE: ATTRIBUTE_PROBE,
                                            ATTRIBUTES_VALUE: value})

    context_element_body = {CONTEXT_TYPE: CONTEXT_SERVER,
                            CONTEXT_IS_PATTERN: CONTEXT_IS_PATTERN_VALUE,
                            CONTEXT_SERVER_ID: server_id,
                            ATTRIBUTES: context_attributes_body}
    return context_element_body


def context_status_code(status_code=None, details='message', reason=CONTEXT_STATUS_CODE_OK):

    """Method to build the status code json
    :param status_code: Numerical status code generated from context server
    :param details: Details regarding the context
    :param reason: Information about the context
    return JSON with status code information (dict)
    """

    status_code_body = {CONTEXT_STATUS_CODE_CODE: status_code,
                        CONTEXT_STATUS_CODE_REASON: reason,
                        CONTEXT_STATUS_CODE_DETAILS: details}

    return status_code_body


def context_response(context_el, status_code):

    """Method to build the JSON with the context element and the status code
    :param context_el: JSON including the context element attributes
    :param status_code: status code received from context manager
    """

    return {CONTEXT_ELEMENT: context_el,
            CONTEXT_STATUS_CODE: status_code}


def context_server(context_responses, originator=None, subscription_id=None):

    """Method to create the JSON with all context responses
    :param context_responses: List with all context responses from server
    :param originator: String with the originator identifier
    :param subscription_id: OpenStack subscription unique identifier
    :returns JSON with all context responses.
    """

    return {SUBSCRIPTION_ID: subscription_id,
            ORIGINATOR: originator,
            CONTEXT_RESPONSES: context_responses}


def build_one_context_server(cpu_value=None, memory_value=None, disk_value=None, network_value=None, server_id=None,
                             subscription_id=None):

    """Method to create a context server body with only one measure.
    :param cpu_value: current value of the CPU
    :param memory_value: current value of the RAM memory
    :param disk_value: current value of the HDD
    :param network_value: current value of the network
    :param server_id: Server unique identifier
    :returns context_server_body:
    """
    context_element_body = context_element(cpu_value, memory_value, disk_value, network_value, server_id)
    context_status_code_body = context_status_code(status_code='200')
    context_response_body = []
    context_response_body.append(context_response(context_element_body, context_status_code_body))
    context_server_body = context_server(context_response_body, None, subscription_id)
    return context_server_body


def delete_all_rules_from_tenant(tenant_id=TENANT_ID):

    """Method to delete all rules from a specific tenant
    :param tenant_id: Tenant unique identifier
    """

    api_utils = RestUtils()
    req = api_utils.retrieve_server_list(tenant_id=tenant_id)
    response = req.json()
    for server in response[SERVERS]:
        server_id = server[SERVER_ID]
        for rule_server in server[RULES]:
            req = api_utils.delete_rule(tenant_id=tenant_id, server_id=server_id,
                                        rule_id=rule_server[RULE_SPECIFIC_ID])
            assert req.ok


def create_subscription(api_utils, server_id=None, headers=HEADERS, tenant_id=TENANT_ID, rule_name=None,
                        rule_condition=None, rule_action=None):

    """Method to subscribe a server to a specific rule not created.
    :param server_id: Server unique identifier
    :param headers: HTTP headers for the requests including authentication
    :param tenant_id: Tenant unique identifier
    :param rule_name: Name of the rule to be created
    :param rule_condition: Condition of the rule to be created
    :param rule_action: Action of the rule to be created
    :returns subscription_id: Subscription unique identifier
    """

    example_rule = {'action': {'actionName': 'notify-scale', 'operation': 'scaleUp'}, 'name': 'aSbKDLIHx', 'condition':
        {'mem': {'operand': 'greater equal', 'value': '98'},
         'net': {'operand': 'greater equal', 'value': '98'},
         'hdd': {'operand': 'greater equal', 'value': '98'},
         'cpu': {'operand': 'greater', 'value': '90'}}}
    rule_id = RestUtils.create_rule(api_utils, tenant_id=tenant_id, server_id=server_id, rule_name=rule_name,
                                    body=example_rule, headers=headers)
    req = api_utils.create_subscription(tenant_id=tenant_id, server_id=server_id,
                                        rule_id=rule_id.json()[RULE_ID], url=RULE_URL_DEFAULT, headers=headers)

    assert_equals(req.status_code, RESPONSE_OK_CODE)
    subscription_id = req.json()[SUBSCRIPTION_ID]
    return subscription_id


def update_context_constant_parameter(parameter, value, context_body):

    """Method to update a parameter inside context JSON
    :param parameter: Parameter to delete
    :param context_body: JSON with all the context body
    :returns Context Body JSON without the parameter updated (dict)
    """

    if parameter == 'isPattern':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_IS_PATTERN] = value
    elif parameter == 'server_type':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_TYPE] = value
    elif parameter == 'name':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_NAME] = value
    elif parameter == 'at_type':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_TYPE] = value

    return context_body


def delete_context_constant_parameter(parameter, context_body):

    """Method to delete a parameter inside context JSON
    :param parameter: Parameter to delete
    :param context_body: JSON with all the context body
    :returns Context Body JSON without the parameter deleted (dict)
    """

    if parameter == 'isPattern':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_IS_PATTERN])
    elif parameter == 'server_type':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_TYPE])
    elif parameter == 'name':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_NAME])
    elif parameter == 'at_type':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_TYPE])

    return context_body


def delete_keys_from_dict(dict_del, key):

    """
    Method to delete keys from python dict
    :param dict_del: Python dictionary with all keys
    :param key: key to be deleted in the Python dictionary
    :returns a new Python dictionary without the rules deleted
    """

    if key in dict_del.keys():

        del dict_del[key]
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, key)

    return dict_del


def replace_values_from_dict(dict_replace, key, replace_to=None):

    """
    Method to replace values from python dict
    :param dict_replace: Python dictionary
    :param key: key to be replaced in the Python dictionary
    :param replace_to: The new value of the keys replaced
    :returns a new Python dictionary without the rules replaced
    """

    if key in dict_replace.keys():

        dict_replace[key] = replace_to
    for v in dict_replace.values():
        if isinstance(v, dict):
            replace_values_from_dict(v, key)

    return dict_replace
