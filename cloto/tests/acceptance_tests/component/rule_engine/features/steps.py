__author__ = 'arobres'


# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from commons.rest_utils import RestUtils
from commons.constants import MOCK_NUM_NOTIFICATIONS, MOCK_NUM_SCALE_UP, MOCK_NUM_SCALE_DOWN
from commons.configuration import HEADERS
import commons.mock_utils as mock_utils
from commons.env_utils import EnvironmentUtils
import commons.authentication as Auth
import commons.utils as Utils
import random

api_utils = RestUtils()
env_utils = EnvironmentUtils()


@before.all
def setup_all():
    env_utils.start_mock()


@before.each_feature
def setup_feature(feature):

    token_id, world.tenant_id = Auth.get_token()
    HEADERS['X-Auth-Token'] = token_id


@before.each_scenario
def setup_scenario(scenario):

    world.headers = HEADERS


@step(u'the window size is "([^"]*)"')
def given_the_window_size_is_group1_in_group2(step, window_size):

    try:
        world.window_size = int(window_size)
    except ValueError:
        print 'Window Size can not be converted to integer'
        world.window_size = window_size

    world.req = api_utils.update_window_size(tenant_id=world.tenant_id, window_size=world.window_size,
                                             headers=world.headers)


@step(u'the following rule subscribed in "([^"]*)"')
def and_the_following_rule_subscribed_in_group1(step, server_id):

    world.count = 0
    mock_utils.reset_responses()
    mock_utils.reset_statistics()

    for examples in step.hashes:

        r_name = examples['name']
        r_condition = examples['condition']
        r_action = examples['action']

        world.subscription_id = Utils.create_subscription(api_utils, server_id=server_id, headers=world.headers,
                                                          rule_name=r_name, tenant_id=world.tenant_id,
                                                          rule_action=r_condition, rule_condition=r_action)


@step(u'context update is received to "([^"]*)" with values "([^"]*)", "([^"]*)", "([^"]*)" and "([^"]*)"')
def send_context_values(step, server_id, cpu, memory, disk, network):

    body = Utils.build_one_context_server(server_id=server_id, cpu_value=cpu, memory_value=memory, disk_value=disk,
                                          network_value=network)

    world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                body=body)


@step(u'the fact is introduced in the Rule Engine')
def then_the_fact_is_introduced_in_the_rule_engine(step):

    response = mock_utils.get_statistics()
    assert int(response[MOCK_NUM_NOTIFICATIONS]) == 1



@step(u'"([^"]*)" of contexts in "([^"]*)"')
def number_contexts_exists(step, number_contexts, server_id):

    at_value = random.random()
    for x in range(int(number_contexts)):
        body = Utils.build_one_context_server(server_id=server_id, cpu_value=at_value, memory_value=at_value,
                                              disk_value=at_value, network_value=at_value)

        world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                    body=body)


@step(u'Then The rule is not fired')
@step(u'the fact is not introduced in the Rule Engine')
def then_the_fact_is_not_introduced_in_the_rule_engine(step):
    response = mock_utils.get_statistics()
    for keys in response.keys():
        assert response[keys] == 0



@step(u'Then The rule is fired with the "([^"]*)"')
def then_the_rule_is_fired(step, action):

    response = mock_utils.get_statistics()
    if action == 'notify':
        assert int(response[MOCK_NUM_NOTIFICATIONS]) == 1
    elif action == 'scale_up':
        assert int(response[MOCK_NUM_SCALE_UP]) == 1
    elif action == 'scale_down':
        assert int(response[MOCK_NUM_SCALE_DOWN]) == 1


@after.all
def setup_all():
    env_utils.stop_mock()