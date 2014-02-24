__author__ = 'artanis'

# -*- coding: utf-8 -*-
from lettuce import step, world, before
from nose.tools import assert_equals, assert_in, assert_true
from commons.rest_utils import RestUtils
from commons.constants import RULE_ID, SERVER_ID
from commons.configuration import HEADERS, TENANT_ID
from commons.errors import HTTP_CODE_NOT_OK, INVALID_JSON, INCORRECT_SERVER_ID, ERROR_CODE_ERROR
import commons.utils as Utils

api_utils = RestUtils()


@before.each_scenario
def setup(scenario):

    #Set default headers with correct token before every scenario
    world.headers = HEADERS


@step(u'a created "([^"]*)" inside tenant')
def set_tenant_and_server_id(step, server_id):

    world.tenant_id = TENANT_ID
    world.server_id = server_id


@step(u'I create a rule with "([^"]*)", "([^"]*)" and "([^"]*)"')
def when_i_create_a_rule_with_group1_group2_and_group3(step, rule_name, rule_condition, rule_action):

    world.rule_name, world.rule_condition, world.rule_action = Utils.create_rule_parameters(rule_name, rule_condition,
                                                                                            rule_action)

    world.req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.rule_name,
                                      condition=world.rule_condition, action=world.rule_action, headers=world.headers)


@step(u'Then the rule is saved in Policy Manager')
def then_the_rule_is_saved_in_policy_manager(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code))
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
def given_a_non_created_group1_and_group2(step, tenant_id, server_id):

    world.tenant_id = tenant_id
    world.server_id = server_id


@step(u'the created rule with "([^"]*)", "([^"]*)" and "([^"]*)" in the "([^"]*)"')
def given_the_created_rule_with_group1_group2_and_group3_in_the_group4(step, rule_name, rule_condition, rule_action,
                                                                       server_id):

    #Save all the expected results in global variables to compare after with obtained results.
    world.tenant_id = TENANT_ID
    world.server_id = server_id
    world.rule_name, world.rule_condition, world.rule_action = Utils.create_rule_parameters(rule_name, rule_condition,
                                                                                            rule_action)
    #Create the rule in Policy Manager
    req = api_utils.create_rule(world.tenant_id, world.server_id, world.rule_name, world.rule_condition,
                                world.rule_action)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code))

    #Save the Rule ID to obtain the Rule information after
    world.rule_id = req.json()[RULE_ID]


@step(u'I retrieve the rule in "([^"]*)"')
def when_i_retrieve_the_rule(step, server_id):

    world.server_id = server_id
    world.req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=world.rule_id,
                                        headers=world.headers)


@step(u'I obtain the Rule data')
def then_i_obtain_the_rule_data(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code))
    response = Utils.assert_json_format(world.req)
    Utils.assert_rule_information(response, world.rule_id, world.rule_name, world.rule_condition, world.rule_action)


@step(u'I retrieve "([^"]*)"')
def when_i_retrieve_group1(step, rule_id):

    world.req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=rule_id,
                                        headers=world.headers)

@step(u'When I delete the rule in "([^"]*)"')
def when_i_delete_the_rule_in_group1(step, server_id):

    world.req = api_utils.delete_rule(tenant_id=world.tenant_id, server_id=server_id, rule_id=world.rule_id,
                                      headers=world.headers)


@step(u'Then the rule is deleted')
def then_the_rule_is_deleted(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code))
    req = api_utils.retrieve_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=world.rule_id,
                                  headers=world.headers)
    assert_equals(req.status_code, 404, ERROR_CODE_ERROR.format(req.status_code, 404))


@step(u'When I delete "([^"]*)"')
def when_i_delete_group1(step, rule_id):

    world.req = api_utils.delete_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_id=rule_id,
                                      headers=world.headers)


@step(u'When I update the rule with "([^"]*)", "([^"]*)" and "([^"]*)" in "([^"]*)"')
def when_i_update_the_rule_with_group1_group2_and_group3_in_group4(step, updated_name, updated_condition,
                                                                   updated_action, server_id):

    world.server_id = server_id

    world.up_name, world.up_condition, world.up_action = Utils.create_rule_parameters(updated_name, updated_condition,
                                                                                      updated_action)

    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.up_name,
                                      condition=world.up_condition, action=world.up_action, rule_id=world.rule_id,
                                      headers=world.headers)

@step(u'Then the rule is updated in Policy Manager')
def then_the_rule_is_updated_in_policy_manager(step):

    assert world.req.ok, world.req.content
    response = Utils.assert_json_format(world.req)
    Utils.assert_rule_information(response=response, rule_id=world.rule_id, name=world.up_name,
                                  condition=world.up_condition, action=world.up_action)


@step(u'When I update "([^"]*)"')
def when_i_update_group1(step, another_rule):

    world.req = api_utils.update_rule(tenant_id=world.tenant_id, server_id=world.server_id, rule_name=world.rule_name,
                                      condition=world.rule_condition, action=world.rule_action, rule_id=another_rule,
                                      headers=world.headers)