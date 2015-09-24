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

# -*- coding: utf-8 -*-
from lettuce import step, world, before
from nose.tools import assert_equals, assert_in, assert_true
from commons.rest_utils import RestUtils
from commons.constants import RULE_ID, SERVER_ID, TENANT_KEY, RULES, SERVERS, RANDOM
from commons.configuration import HEADERS
from commons.errors import HTTP_CODE_NOT_OK, INVALID_JSON, INCORRECT_SERVER_ID, ERROR_CODE_ERROR
import commons.authentication as Auth
import commons.utils as Utils
import commons.rule_utils as Rule_Utils
import random

api_utils = RestUtils()


@before.each_feature
def setup_feature(feature):

    token_id, world.tenant_id = Auth.get_token()
    HEADERS['X-Auth-Token'] = token_id


@before.each_scenario
def setup_scenario(scenario):

    world.headers = HEADERS
    Utils.delete_all_rules_from_tenant()
    world.rules = []


@step(u'a created "([^"]*)" inside tenant')
def set_tenant_and_server_id(step, server_id):

    world.server_id = server_id
    world.cpu = None
    world.mem = None
    world.hdd = None
    world.net = None


@step(u'the rule is saved in Policy Manager')
def assert_rule_saved(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = world.req.json()
    assert_equals(response[SERVER_ID], world.server_id, INCORRECT_SERVER_ID.format(world.server_id,
                                                                                   response[SERVER_ID]))
    assert_in(RULE_ID, response.keys(), INVALID_JSON.format(response))


@step(u'I obtain an "([^"]*)" and the "([^"]*)"')
def assert_error_response(step, error_code, fault_element):

    Utils.assert_error_code_error(response=world.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'incorrect "([^"]*)"')
def set_incorrect_token(step, token):

    #Set and incorrect header to obtain unauthorized error
    world.headers = Utils.create_header(token=token)


@step(u'a non created "([^"]*)" and "([^"]*)"')
def set_non_existent_tenant_and_server(step, tenant_id, server_id):

    world.tenant_id = tenant_id
    world.server_id = server_id


@step(u'I retrieve the rule in "([^"]*)"')
def retrieve_rule(step, server_id):

    world.server_id = server_id
    world.req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=world.rule_id,
                                        headers=world.headers)


@step(u'I obtain the Rule data')
def assert_rule_information(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = Utils.assert_json_format(world.req)
    Rule_Utils.assert_rule_information(response=response, rule_id=world.rule_id, body=world.rule_body)


@step(u'I retrieve "([^"]*)"')
def retrieve_specific_rule(step, rule_id):

    world.req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=rule_id,
                                        headers=world.headers)


@step(u'I delete the rule in "([^"]*)"')
def delete_rule(step, server_id):

    world.req = api_utils.delete_rule(tenant_id=world.tenant_id, server_id=server_id, rule_id=world.rule_id,
                                      headers=world.headers)


@step(u'the rule is deleted')
def assert_rule_is_deleted(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=world.rule_id,
                                  headers=world.headers)
    assert_equals(req.status_code, 404, ERROR_CODE_ERROR.format(req.status_code, 404))


@step(u'When I delete "([^"]*)"')
def delete_specific_rule(step, rule_id):

    world.req = api_utils.delete_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=rule_id,
                                      headers=world.headers)


@step(u'I update the rule with "([^"]*)", "([^"]*)" and "([^"]*)" in "([^"]*)"')
def update_rule(step, updated_name, updated_condition, updated_action, server_id):

    world.server_id = server_id

    world.up_name, world.up_condition, world.up_action = Utils.create_rule_parameters(updated_name, updated_condition,
                                                                                      updated_action)

    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.up_name,
                                      condition=world.up_condition, action=world.up_action, rule_id=world.rule_id,
                                      headers=world.headers)


@step(u'the rule is updated in Policy Manager')
def assert_rule_is_updated(step):

    assert world.req.ok, world.req.content
    response = Utils.assert_json_format(world.req)
    Rule_Utils.assert_rule_information(response=response, rule_id=world.rule_id, name=world.rule_name, cpu=world.cpu,
                                  mem=world.mem, hdd=world.hdd, net=world.net, action=world.rule_action)


@step(u'I update "([^"]*)"')
def update_non_existent_rule(step, another_rule):

    body = Rule_Utils.create_notify_specific_rule()
    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=body,
                                      rule_id=another_rule, headers=world.headers)


@step(u'I get the rules list from "([^"]*)"')
def when_i_get_the_rules_list_from_group1(step, server_id):

    world.server_id = server_id
    world.req = api_utils.retrieve_rules(tenant_id=world.tenant_id, server_id=world.server_id, headers=world.headers)


@step(u'Then I obtain all the rules of the server')
def then_i_obtain_all_the_rules_of_the_server(step):

    response = Utils.assert_json_format(world.req)

    assert_equals(response[SERVER_ID], world.server_id)
    assert_equals(response[TENANT_KEY], world.tenant_id)
    assert_equals(len(response[RULES]), world.number_rules)

    for rule, u_response in zip(world.rules, response[RULES]):
        assert_in(rule['name'], u_response['name'])
    world.rules = []
    Utils.delete_all_rules_from_tenant()


@step(u'Given "([^"]*)" of rules created in "([^"]*)"')
def given_group1_of_rules_created_in_group2(step, number_rules, server_id):

    world.server_id = server_id
    world.number_rules = int(number_rules)
    for x in range(world.number_rules):
        rule_body = Rule_Utils.create_notify_specific_rule()
        req = api_utils.create_rule(world.tenant_id, world.server_id, body=rule_body)
        assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
        rule_id = req.json()[RULE_ID]
        world.rules.append(rule_body)


@step(u'Then I obtain zero rules')
def then_i_obtain_zero_rules(step):

    response = Utils.assert_json_format(world.req)

    assert_equals(response[SERVER_ID], world.server_id)
    assert_equals(response[TENANT_KEY], world.tenant_id)
    assert_equals(len(response[RULES]), 0)


@step(u'Given a created "([^"]*)" without rules')
def given_a_created_group1_without_rules(step, server_id):

    world.server_id = server_id
    created_rule(step, server_id=world.server_id)
    delete_rule(step, server_id=world.server_id)
    world.servers_body = [{SERVER_ID: world.server_id,
                           RULES: []}]


@step(u'Given a tenant without servers')
def given_a_tenant_without_servers(step):

    pass


@step(u'When I retrieve the server list')
def when_i_retrieve_the_server_list(step):
    world.req = api_utils.retrieve_server_list(tenant_id=world.tenant_id, headers=world.headers)


@step(u'Then I obtain zero results')
def then_i_obtain_zero_results(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = Utils.assert_json_format(world.req)
    assert_equals(response[SERVERS], [])


@step(u'Given a "([^"]*)" of servers in a tenant with rules created')
def given_a_group1_of_servers_in_a_tenant(step, number_servers):

    world.number_servers = int(number_servers)
    world.servers_body = []

    for x in range(world.number_servers):
        world.rules = []
        server_id = Utils.id_generator(size=6)
        number_rules = random.randint(1, 5)

        for rule in range(number_rules):
            rule_body = Rule_Utils.create_scale_specific_rule()
            req = api_utils.create_rule(world.tenant_id, server_id, body=rule_body)
            assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
            rule_id = req.json()[RULE_ID]
            world.rules.append(Rule_Utils.create_rule_body(action=None, rule_id=rule_id, condition=None,
                                                           name=rule_body['name']))

        server_dict = {SERVER_ID: server_id,
                       RULES: world.rules}
        world.servers_body.append(server_dict)


@step(u'Then I obtain the server list')
def then_i_obtain_the_server_list(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = Utils.assert_json_format(world.req)
    for results in world.servers_body:
        assert_in(results, response[SERVERS])
    Utils.delete_all_rules_from_tenant()


@step(u'And parameter "([^"]*)" with "([^"]*)" and "([^"]*)"')
def and_parameter_group1_with_group2_and_group3(step, parameter_name, parameter_value, parameter_operand):

    if parameter_name == 'cpu':
        world.cpu = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'mem':
        world.mem = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'hdd':
        world.hdd = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)

    elif parameter_name == 'net':
        world.net = Rule_Utils.create_rule_parameter_dict(value=parameter_value, operand=parameter_operand)


@step(u'When I create a scale rule with "([^"]*)" and "([^"]*)"')
def when_i_create_a_scale_rule_with_group1_and_group2(step, rule_name, action):

    if rule_name == 'random':
        rule_name = Utils.id_generator()

    action = Rule_Utils.create_rule_action_dict(action_name='notify-scale', operation=action)

    world.req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=rule_name,
                                      cpu=world.cpu, mem=world.mem, hdd=world.hdd, net=world.net, action=action,
                                      headers=world.headers)


@step(u'When I create a notify rule with "([^"]*)", "([^"]*)" and "([^"]*)"')
def when_i_create_a_notify_rule_with_group1_group2_and_group3(step, rule_name, body, email):

    action = Rule_Utils.create_rule_action_dict(action_name='notify-email', body=body, email=email)

    world.req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=rule_name,
                                      cpu=world.cpu, mem=world.mem, hdd=world.hdd, net=world.net, action=action,
                                      headers=world.headers)


@step(u'And some rule prepared with all data')
def and_some_rule_prepared_with_all_data(step):

    world.rule_body = Rule_Utils.create_scale_specific_rule()


@step(u'And the "([^"]*)" deleted')
def and_the_group1_deleted(step, key):

    world.rule_body = Utils.delete_keys_from_dict(dict_del=world.rule_body, key=key)


@step(u'When I create an incorrect rule')
def when_i_create_an_incorrect_rule(step):

    world.req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=world.rule_body,
                                          headers=world.headers)


@step(u'And the "([^"]*)" replaced to "([^"]*)"')
def and_the_group1_replaced_to_none(step, key, to_replace):

    if to_replace == 'None':
        world.rule_body = Utils.replace_values_from_dict(dict_replace=world.rule_body, key=key)
    else:
        world.rule_body = Utils.replace_values_from_dict(dict_replace=world.rule_body, key=key, replace_to=to_replace)


@step(u'Given a created rule in the in the "([^"]*)"')
def created_rule(step, server_id):

    world.server_id = server_id
    world.rule_body = Rule_Utils.create_scale_specific_rule()

    #Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=world.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    #Save the Rule ID to obtain the Rule information after
    world.rule_id = req.json()[RULE_ID]


@step(u'Given the created scale rule in the in the "([^"]*)" with the following parameters')
def given_the_created_scale_rule_in_the_in_the_group1_with_the_following_parameters(step, server_id):

    world.cpu = None
    world.mem = None
    world.hdd = None
    world.net = None
    world.server_id = server_id

    for examples in step.hashes:
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

        req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=rule_body)
        world.rule_id = req.json()[RULE_ID]


@step(u'When I update the scalability rule with "([^"]*)" and "([^"]*)" in "([^"]*)"')
def when_i_update_the_rule_with_group1_and_group2(step, new_name, new_action, server_id):

    if new_name == 'random':
        world.rule_name = Utils.id_generator()
    else:
        world.rule_name = new_name

    world.server_id = server_id

    world.rule_action = Rule_Utils.create_rule_action_dict(action_name='notify-scale', operation=new_action)

    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.rule_name,
                                      cpu=world.cpu, mem=world.mem, hdd=world.hdd, net=world.net,
                                      action=world.rule_action, headers=world.headers, rule_id=world.rule_id)


@step(u'Given the created notify rule in the in the "([^"]*)" with the following parameters')
def given_the_created_notify_rule_in_the_in_the_group1_with_the_following_parameters(step, server_id):
    world.cpu = None
    world.mem = None
    world.hdd = None
    world.net = None
    world.server_id = server_id

    for examples in step.hashes:
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

        req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=rule_body)
        world.rule_id = req.json()[RULE_ID]


@step(u'When I update the notify rule with "([^"]*)", "([^"]*)" and "([^"]*)" in "([^"]*)"')
def when_i_update_the_notify_rule_with_group1_group2_and_group3(step, new_name, new_body, new_mail, server_id):

    if new_name == RANDOM:
        world.rule_name = Utils.id_generator()
    else:
        world.rule_name = new_name
    world.server_id = server_id

    world.rule_action = Rule_Utils.create_rule_action_dict(action_name='notify-email', body=new_body, email=new_mail)

    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.rule_name,
                                      cpu=world.cpu, mem=world.mem, hdd=world.hdd, net=world.net,
                                      action=world.rule_action, headers=world.headers, rule_id=world.rule_id)
