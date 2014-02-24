__author__ = 'artanis'

# -*- coding: utf-8 -*-
from lettuce import step, world, before
from nose.tools import assert_equals, assert_in, assert_true
from commons.rest_utils import RestUtils
from commons.constants import RULE_ID, SERVER_ID, SUBSCRIPTION_ID
from commons.configuration import HEADERS, TENANT_ID
from commons.errors import HTTP_CODE_NOT_OK, INVALID_JSON, INCORRECT_SERVER_ID, ERROR_CODE_ERROR
import commons.utils as Utils

api_utils = RestUtils()


@before.each_scenario
def setup(scenario):

    #Set default headers with correct token before every scenario
    world.headers = HEADERS


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


@step(u'When I create a new subscription in "([^"]*)" with "([^"]*)"')
def when_i_create_a_new_subscription_with_group1(step, server_id, url_to_notify):

    world.server_id = server_id
    world.url_to_notify = url_to_notify
    world.req = api_utils.create_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                              rule_id=world.rule_id, url=world.url_to_notify)


@step(u'Then the subscription is created')
def then_the_subscription_is_created(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code))
    response = Utils.assert_json_format(world.req)
    assert_equals(response[SERVER_ID], world.server_id)
    assert_in(SUBSCRIPTION_ID, response.keys())


@step(u'I obtain an "([^"]*)" and the "([^"]*)"')
def assert_error_response(step, error_code, fault_element):

    Utils.assert_error_code_error(response=world.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'Given the rule "([^"]*)"')
def given_the_rule_group1(step, rule_id):

    world.tenant_id = TENANT_ID
    world.rule_id = rule_id
