#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014-2016 Telefónica Investigación y Desarrollo, S.A.U
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
# -*- coding: utf-8 -*-
import behave
from behave import step
from nose.tools import assert_equals, assert_in, assert_true
from commons.rest_utils import RestUtils
from commons.constants import RULE_ID, SERVER_ID, TENANT_KEY, RULES, SERVERS, RANDOM
from commons.errors import HTTP_CODE_NOT_OK, INVALID_JSON, INCORRECT_SERVER_ID, ERROR_CODE_ERROR
import commons.utils as Utils
import commons.rule_utils as Rule_Utils
import random

api_utils = RestUtils()
behave.use_step_matcher("re")


@step(u'a created server with serverid "([^"]*)" inside a tenant')
@step(u'a created server with server id "([^"]*)" inside a tenant')
def set_tenant_and_server_id(context, server_id):

    context.server_id = server_id
    context.cpu = None
    context.mem = None
    context.hdd = None
    context.net = None


@step(u'the rule is saved in Policy Manager')
def assert_rule_saved(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))

    response = context.req.json()

    assert_equals(response[SERVER_ID],
                  context.server_id,
                  INCORRECT_SERVER_ID.format(context.server_id, response[SERVER_ID])
                  )

    assert_in(RULE_ID, response.keys(), INVALID_JSON.format(response))


@step(u'I obtain an error code "([^"]*)" and the fault element "([^"]*)"')
def assert_error_response(context, error_code, fault_element):

    Utils.assert_error_code_error(response=context.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'an incorrect token with value "([^"]*)"')
def set_incorrect_token(context, token):

    # Set and incorrect header to obtain unauthorized error
    context.headers = Utils.create_header(token=token)


@step(u'a non created tenant with id "([^"]*)" and server with id "([^"]*)"')
def set_non_existent_tenant_and_server(context, tenant_id, server_id):

    context.tenant_id = tenant_id
    context.server_id = server_id


@step(u'I request the rule from the server with id "([^"]*)"')
@step(u'I request the rule from other server with id "([^"]*)"')
def retrieve_rule(context, server_id):

    context.server_id = server_id
    context.req = api_utils.retrieve_rule(tenant_id=context.tenant_id, server_id=context.server_id,
                                          rule_id=context.rule_id, headers=context.headers)


@step(u'I obtain the Rule data')
def assert_rule_information(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))

    response = Utils.assert_json_format(context.req)
    Rule_Utils.assert_rule_information(response=response, rule_id=context.rule_id, body=context.rule_body)


@step(u'I request other rule with id "([^"]*)"')
def retrieve_specific_rule(context, rule_id):

    context.req = api_utils.retrieve_rule(tenant_id=context.tenant_id, server_id=context.server_id, rule_id=rule_id,
                                          headers=context.headers)


@step(u'I delete the rule in the server with id "([^"]*)"')
@step(u'I delete the rule in other server with id "([^"]*)"')
def delete_rule(context, server_id):

    context.req = api_utils.delete_rule(tenant_id=context.tenant_id, server_id=server_id, rule_id=context.rule_id,
                                        headers=context.headers)


@step(u'the rule is deleted')
def assert_rule_is_deleted(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))

    req = api_utils.retrieve_rule(tenant_id=context.tenant_id, server_id=context.server_id, rule_id=context.rule_id,
                                  headers=context.headers)

    assert_equals(req.status_code, 404, ERROR_CODE_ERROR.format(req.status_code, 404))


@step(u'I delete other rule with id "([^"]*)"')
def delete_specific_rule(context, rule_id):

    context.req = api_utils.delete_rule(tenant_id=context.tenant_id, server_id=context.server_id, rule_id=rule_id,
                                        headers=context.headers)


@step(u'I update the rule with "([^"]*)", "([^"]*)" and "([^"]*)" in "([^"]*)"')
def update_rule(context, updated_name, updated_condition, updated_action, server_id):

    context.server_id = server_id

    context.up_name, context.up_condition, context.up_action = \
        Utils.create_rule_parameters(updated_name, updated_condition, updated_action)

    context.req = api_utils.update_rule(tenant_id=context.tenant_id, server_id=context.server_id,
                                        rule_name=context.up_name, condition=context.up_condition,
                                        action=context.up_action, rule_id=context.rule_id,
                                        headers=context.headers)


@step(u'the rule is updated in Policy Manager')
def assert_rule_is_updated(context):

    assert context.req.ok, context.req.content

    response = Utils.assert_json_format(context.req)
    Rule_Utils.assert_rule_information(response=response, rule_id=context.rule_id, name=context.rule_name,
                                       cpu=context.cpu, mem=context.mem, hdd=context.hdd, net=context.net,
                                       action=context.rule_action)


@step(u'I update "([^"]*)"')
def update_non_existent_rule(context, another_rule):

    body = Rule_Utils.create_notify_specific_rule()
    context.req = api_utils.update_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=body,
                                        rule_id=another_rule, headers=context.headers)


@step(u'I get the rules list from server with server id "([^"]*)"')
def when_i_get_the_rules_list_from_group1(context, server_id):

    context.server_id = server_id
    context.req = api_utils.retrieve_rules(tenant_id=context.tenant_id, server_id=context.server_id,
                                           headers=context.headers)


@step(u'I obtain all the rules of the server')
def then_i_obtain_all_the_rules_of_the_server(context):

    response = Utils.assert_json_format(context.req)

    assert_equals(response[SERVER_ID], context.server_id)
    assert_equals(response[TENANT_KEY], context.tenant_id)
    assert_equals(len(response[RULES]), context.number_rules)

    for rule, u_response in zip(context.rules, response[RULES]):
        assert_in(rule['name'], u_response['name'])
    context.rules = []
    Utils.delete_all_rules_from_tenant()


@step(u'"([^"]*)" rules created in a server with server id "([^"]*)"')
@step(u'"([^"]*)" rule created in a server with server id "([^"]*)"')
def given_group1_of_rules_created_in_group2(context, number_rules, server_id):

    context.server_id = server_id
    context.number_rules = int(number_rules)
    for x in range(context.number_rules):
        rule_body = Rule_Utils.create_notify_specific_rule()
        req = api_utils.create_rule(context.tenant_id, context.server_id, body=rule_body)
        assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
        req.json()[RULE_ID]
        context.rules.append(rule_body)


@step(u'I obtain zero rules')
def then_i_obtain_zero_rules(context):

    response = Utils.assert_json_format(context.req)

    assert_equals(response[SERVER_ID], context.server_id)
    assert_equals(response[TENANT_KEY], context.tenant_id)
    assert_equals(len(response[RULES]), 0)


@step(u'a created server with server id "([^"]*)" without rules')
def given_a_created_group1_without_rules(context, server_id):

    context.server_id = server_id
    created_rule(context, server_id=context.server_id)
    delete_rule(context, server_id=context.server_id)
    context.servers_body = [{SERVER_ID: context.server_id, RULES: []}]


@step(u'a tenant without servers')
def given_a_tenant_without_servers(context):

    pass


@step(u'I retrieve the server list')
def when_i_retrieve_the_server_list(context):
    context.req = api_utils.retrieve_server_list(tenant_id=context.tenant_id, headers=context.headers)


@step(u'I obtain zero results')
def then_i_obtain_zero_results(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))

    response = Utils.assert_json_format(context.req)
    assert_equals(response[SERVERS], [])


@step(u'a number of servers equat to "([^"]*)" in a tenant with rules created')
def given_a_group1_of_servers_in_a_tenant(context, number_servers):

    context.number_servers = int(number_servers)
    context.servers_body = []

    for x in range(context.number_servers):
        context.rules = []
        server_id = Utils.id_generator(size=6)
        number_rules = random.randint(1, 5)

        for rule in range(number_rules):
            rule_body = Rule_Utils.create_scale_specific_rule()
            req = api_utils.create_rule(context.tenant_id, server_id, body=rule_body)
            assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
            rule_id = req.json()[RULE_ID]
            context.rules.append(Rule_Utils.create_rule_body(action=None, rule_id=rule_id, condition=None,
                                                             name=rule_body['name']))

        server_dict = {SERVER_ID: server_id,
                       RULES: context.rules}
        context.servers_body.append(server_dict)


@step(u'I obtain the server list')
@step(u'I obtain the server list without rules')
def then_i_obtain_the_server_list(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))
    response = Utils.assert_json_format(context.req)
    for results in context.servers_body:
        assert_in(results, response[SERVERS])
    Utils.delete_all_rules_from_tenant()


@step(u'parameter "([^"]*)" with value "([^"]*)" and operand "([^"]*)"')
def and_parameter_group1_with_group2_and_group3(context, parameter_name, parameter_value, parameter_operand):

    if parameter_name == 'cpu':
        context.cpu = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'mem':
        context.mem = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'hdd':
        context.hdd = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'net':
        context.net = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)


@step(u'I create a scale rule with name "([^"]*)" and action "([^"]*)"')
def when_i_create_a_scale_rule_with_group1_and_group2(context, rule_name, action):

    if rule_name == 'random':
        rule_name = Utils.id_generator()

    action = Rule_Utils.create_rule_action_dict(action_name='notify-scale', operation=action)

    context.req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, rule_name=rule_name,
                                        cpu=context.cpu, mem=context.mem, hdd=context.hdd, net=context.net,
                                        action=action, headers=context.headers)


@step(u'I create a notify rule with name "([^"]*)", body "([^"]*)" and email "([^"]*)"')
def when_i_create_a_notify_rule_with_group1_group2_and_group3(context, rule_name, body, email):

    action = Rule_Utils.create_rule_action_dict(action_name='notify-email', body=body, email=email)

    context.req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, rule_name=rule_name,
                                        cpu=context.cpu, mem=context.mem, hdd=context.hdd, net=context.net,
                                        action=action, headers=context.headers)


@step(u'some rule prepared with all data')
def and_some_rule_prepared_with_all_data(context):

    context.rule_body = Rule_Utils.create_scale_specific_rule()


@step(u'the "([^"]*)" deleted')
def and_the_group1_deleted(context, key):

    context.rule_body = Utils.delete_keys_from_dict(dict_del=context.rule_body, key=key)


@step(u'I create an incorrect rule')
def when_i_create_an_incorrect_rule(context):

    context.req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id,
                                        body=context.rule_body, headers=context.headers)


@step(u'the parameter "([^"]*)" replaced to "([^"]*)"')
def and_the_group1_replaced_to_none(context, key, to_replace):

    if to_replace == 'None':
        context.rule_body = Utils.replace_values_from_dict(dict_replace=context.rule_body, key=key)
    else:
        context.rule_body = Utils.replace_values_from_dict(dict_replace=context.rule_body,
                                                           key=key,
                                                           replace_to=to_replace)


@step(u'a created rule in the server with id "([^"]*)"')
def created_rule(context, server_id):

    context.server_id = server_id
    context.rule_body = Rule_Utils.create_scale_specific_rule()

    # Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=context.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    # Save the Rule ID to obtain the Rule information after
    context.rule_id = req.json()[RULE_ID]


@step(u'the created scale rule in the server with id "([^"]*)" with the following parameters')
def given_the_created_scale_rule_in_the_in_the_group1_with_the_following_parameters(context, server_id):

    context.cpu = None
    context.mem = None
    context.hdd = None
    context.net = None
    context.server_id = server_id

    for examples in context.table.rows:
        rule_body = Rule_Utils.create_scale_specific_rule(operation=examples['operation'],
                                                          name=examples['name'],
                                                          cpu_value=examples['cpu_value'],
                                                          cpu_operand=examples['cpu_operand'],
                                                          mem_value=examples['mem_value'],
                                                          mem_operand=examples['mem_operand'],
                                                          hdd_value=examples['hdd_value'],
                                                          hdd_operand=examples['hdd_operand'],
                                                          net_value=examples['net_value'],
                                                          net_operand=examples['net_operand'])

        req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=rule_body)
        context.rule_id = req.json()[RULE_ID]


@step(u'I update the scalability rule with "([^"]*)" and "([^"]*)" in "([^"]*)"')
def when_i_update_the_rule_with_group1_and_group2(context, new_name, new_action, server_id):

    if new_name == 'random':
        context.rule_name = Utils.id_generator()
    else:
        context.rule_name = new_name

    context.server_id = server_id

    context.rule_action = Rule_Utils.create_rule_action_dict(action_name='notify-scale', operation=new_action)

    context.req = api_utils.update_rule(tenant_id=context.tenant_id, server_id=context.server_id,
                                        rule_name=context.rule_name, cpu=context.cpu, mem=context.mem,
                                        hdd=context.hdd, net=context.net, action=context.rule_action,
                                        headers=context.headers, rule_id=context.rule_id)


@step(u'the created notify rule in the server with id "([^"]*)" with the following parameters')
def given_the_created_notify_rule_in_the_in_the_group1_with_the_following_parameters(context, server_id):
    context.cpu = None
    context.mem = None
    context.hdd = None
    context.net = None
    context.server_id = server_id

    for examples in context.table.rows:
        rule_body = Rule_Utils.create_notify_specific_rule(body=examples['body'],
                                                           email=examples['email'],
                                                           name=examples['name'],
                                                           cpu_value=examples['cpu_value'],
                                                           cpu_operand=examples['cpu_operand'],
                                                           mem_value=examples['mem_value'],
                                                           mem_operand=examples['mem_operand'],
                                                           hdd_value=examples['hdd_value'],
                                                           hdd_operand=examples['hdd_operand'],
                                                           net_value=examples['net_value'],
                                                           net_operand=examples['net_operand'])

        req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=rule_body)
        context.rule_id = req.json()[RULE_ID]


@step(u'I update the notify rule with "([^"]*)", "([^"]*)" and "([^"]*)" in "([^"]*)"')
def when_i_update_the_notify_rule_with_group1_group2_and_group3(context, new_name, new_body, new_mail, server_id):

    if new_name == RANDOM:
        context.rule_name = Utils.id_generator()
    else:
        context.rule_name = new_name
    context.server_id = server_id

    context.rule_action = Rule_Utils.create_rule_action_dict(action_name='notify-email', body=new_body, email=new_mail)

    context.req = api_utils.update_rule(tenant_id=context.tenant_id, server_id=context.server_id,
                                        rule_name=context.rule_name, cpu=context.cpu, mem=context.mem,
                                        hdd=context.hdd, net=context.net, action=context.rule_action,
                                        headers=context.headers, rule_id=context.rule_id)
