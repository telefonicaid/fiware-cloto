__author__ = 'arobres'


# -*- coding: utf-8 -*-
from lettuce import step, world, before
from nose.tools import assert_true
from commons.rest_utils import RestUtils
from commons.constants import RANDOM, DEFAULT
from commons.configuration import HEADERS
from commons.errors import HTTP_CODE_NOT_OK
import commons.authentication as Auth
import commons.utils as Utils

api_utils = RestUtils()


@before.each_feature
def setup_feature(feature):

    token_id, world.tenant_id = Auth.get_token()
    HEADERS['X-Auth-Token'] = token_id


@before.each_scenario
def setup_scenario(scenario):

    world.headers = HEADERS


@step(u'Given a "([^"]*)" with one rule subscribed')
def given_a_group1_with_one_rule_subscribed(step, server_id):

    world.server_id = server_id

    world.subscription_id = Utils.create_subscription(api_utils, server_id=server_id, headers=HEADERS, rule_name=RANDOM,
                                                      tenant_id=world.tenant_id, rule_action=DEFAULT,
                                                      rule_condition=DEFAULT)


@step(u'When context update is received to "([^"]*)" with values "([^"]*)", "([^"]*)", "([^"]*)" and "([^"]*)"')
def send_context_values(step, server_id, cpu, memory, disk, network):

    world.cpu = cpu
    world.memory = memory
    world.disk = disk
    world.network = network
    body = Utils.build_one_context_server(server_id=server_id, cpu_value=cpu, memory_value=memory, disk_value=disk,
                                          network_value=network)

    world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                body=body)


@step(u'Then the context is updated')
def then_the_context_is_updated(step):

    print world.req.content
    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code))


@step(u'Then I obtain an "([^"]*)" and the "([^"]*)"')
def then_i_obtain_an_group1_and_the_group2(step, error_code, fault_element):

    Utils.assert_error_code_error(response=world.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'And another "([^"]*)" that not exist')
def and_another_group1_that_not_exist(step, subscription_id):

    world.subscription_id = subscription_id


@step(u'When context updated is receiver to "([^"]*)" with constant "([^"]*)" incorrect')
def when_context_updated_is_receiver_to_group1_with_constant_group2_incorrect(step, server_id, parameter):

    body = Utils.build_one_context_server(server_id=server_id, cpu_value='0.1', memory_value='0.1', disk_value='0.1',
                                          network_value='0.1')

    body = Utils.update_context_constant_parameter(parameter=parameter, value='qa', context_body=body)

    world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                body=body)


@step(u'When context updated is receiver to "([^"]*)" with missing constant "([^"]*)"')
def when_context_updated_is_receiver_to_group1_with_missing_constant_group2(step, server_id, parameter):

    body = Utils.build_one_context_server(server_id=server_id, cpu_value='0.1', memory_value='0.1', disk_value='0.1',
                                          network_value='0.1')

    body = Utils.delete_context_constant_parameter(parameter=parameter, context_body=body)

    world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                body=body)


@step(u'incorrect "([^"]*)"')
def set_incorrect_token(step, token):

    #Set and incorrect header to obtain unauthorized error
    world.headers = Utils.create_header(token=token)
