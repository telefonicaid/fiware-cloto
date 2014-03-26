__author__ = 'arobres'


# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from nose.tools import assert_true
from commons.rest_utils import RestUtils
from commons.constants import RANDOM, DEFAULT
from commons.configuration import HEADERS
from commons.errors import HTTP_CODE_NOT_OK
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
    #TODO assertion in Rabbit or Firing the RULE
    pass


@step(u'"([^"]*)" of contexts in "([^"]*)"')
def number_contexts_exists(step, number_contexts, server_id):

    at_value = random.random()
    for x in range(int(number_contexts)):
        body = Utils.build_one_context_server(server_id=server_id, cpu_value=at_value, memory_value=at_value,
                                              disk_value=at_value, network_value=at_value)

        world.req = api_utils.update_server_context(tenant_id=world.tenant_id, headers=world.headers, server_id=server_id,
                                                    body=body)


@step(u'the fact is not introduced in the Rule Engine')
def then_the_fact_is_not_introduced_in_the_rule_engine(step):
    #TODO assertion in Rabbit or Not Firing the RULE
    pass


@step(u'Then The rule is fired')
def then_the_rule_is_fired(step):
    #TODO assertion using the HTTP mock to verify the HTTP REST request is sent
    pass


@step(u'Then The rule is not fired')
def then_the_rule_is_not_fired(step):
    #TODO assertion using the HTTP mock to verify the HTTP REST request is not sent
    pass


@after.all
def setup_all():
    env_utils.stop_mock()