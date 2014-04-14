__author__ = 'artanis'

# -*- coding: utf-8 -*-
from lettuce import step, world, before
from nose.tools import assert_equals, assert_in, assert_true
from commons.rest_utils import RestUtils
from commons.constants import RULE_ID, SERVER_ID, SUBSCRIPTION_ID, RANDOM, DEFAULT, RULE_URL_DEFAULT, \
    ITEM_NOT_FOUND_ERROR, RULE_URL
from commons.configuration import HEADERS, TENANT_ID
from commons.errors import HTTP_CODE_NOT_OK
import commons.utils as Utils
import commons.rule_utils as Rule_Utils
import commons.authentication as Auth

api_utils = RestUtils()


@before.each_feature
def setup_feature(feature):

    token_id, world.tenant_id = Auth.get_token()
    HEADERS['X-Auth-Token'] = token_id


@before.each_scenario
def setup_scenario(scenario):

    world.headers = HEADERS


@step(u'Given a created rule in the in the "([^"]*)"')
def created_rule(step, server_id):

    world.server_id = server_id
    world.rule_body = Rule_Utils.create_scale_specific_rule()

    #Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=world.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    #Save the Rule ID to obtain the Rule information after
    world.rule_id = req.json()[RULE_ID]


@step(u'I create a new subscription in "([^"]*)" with "([^"]*)"')
def new_subscription_in_server(step, server_id, url_to_notify):

    world.url_to_notify = url_to_notify
    if server_id == RANDOM:
        world.server_id = Utils.id_generator(10)
    else:
        world.server_id = server_id

    world.req = api_utils.create_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                              rule_id=world.rule_id, url=world.url_to_notify, headers=world.headers)


@step(u'I create the same subscription')
def create_subscription_created_before(step):

    world.req = api_utils.create_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                              rule_id=world.rule_id, url=world.url_to_notify, headers=world.headers)


@step(u'the subscription is created')
def assert_subscription_created(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = Utils.assert_json_format(world.req)
    assert_equals(response[SERVER_ID], world.server_id)
    assert_in(SUBSCRIPTION_ID, response.keys())


@step(u'I obtain an "([^"]*)" and the "([^"]*)"')
def assert_error_response(step, error_code, fault_element):

    Utils.assert_error_code_error(response=world.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'the rule "([^"]*)"')
def given_the_rule(step, rule_id):

    world.tenant_id = TENANT_ID
    world.rule_id = rule_id


@step(u'incorrect "([^"]*)"')
def set_incorrect_token(step, token):

    #Set and incorrect header to obtain unauthorized error
    world.headers = Utils.create_header(token=token)


@step(u'a subscription created in "([^"]*)"')
def created_subscription(step, server_id):

    world.tenant_id = TENANT_ID
    world.server_id = server_id
    world.headers = HEADERS

    world.rule_body = Rule_Utils.create_scale_specific_rule()

    #Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=world.tenant_id, server_id=world.server_id, body=world.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    #Save the Rule ID to obtain the Rule information after
    world.rule_id = req.json()[RULE_ID]

    req = api_utils.create_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                        rule_id=world.rule_id, url=RULE_URL_DEFAULT, headers=world.headers)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
    print req.content
    world.subscription_id = req.json()[SUBSCRIPTION_ID]


@step(u'I delete a subscription in "([^"]*)"')
def delete_subscription_in_server(step, server_id):

    if server_id == RANDOM:
        world.server_id = Utils.id_generator(10)
    else:
        world.server_id = server_id

    world.req = api_utils.delete_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                              subscription_id=world.subscription_id, headers=world.headers)


@step(u'the subscription is deleted')
def assert_subscription_is_deleted(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    req = api_utils.retrieve_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                          subscription_id=world.subscription_id, headers=world.headers)
    Utils.assert_error_code_error(response=req, expected_error_code='404',
                                  expected_fault_element=ITEM_NOT_FOUND_ERROR)


@step(u'I delete a not existent subscription in "([^"]*)"')
def delete_non_existent_subscription(step, server_id):

    world.server_id = server_id
    world.req = api_utils.delete_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                              subscription_id=Utils.id_generator(10), headers=world.headers)


@step(u'I retrieve the subscription in "([^"]*)"')
def retrieve_subscription(step, server_id):

    if server_id == RANDOM:
        world.server_id = Utils.id_generator(10)
    else:
        world.server_id = server_id

    world.req = api_utils.retrieve_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                                subscription_id=world.subscription_id, headers=world.headers)


@step(u'I get all subscription information')
def assert_subscription_information(step):

    assert_true(world.req.ok, HTTP_CODE_NOT_OK.format(world.req.status_code, world.req.content))
    response = Utils.assert_json_format(world.req)
    assert_equals(response[RULE_URL], RULE_URL_DEFAULT)
    assert_equals(response[SERVER_ID], world.server_id)
    assert_equals(response[SUBSCRIPTION_ID], world.subscription_id)
    assert_equals(response[RULE_ID], world.rule_id)


@step(u'I retrieve a not existent subscription in "([^"]*)"')
def retrieve_non_existent_subscription(step, server_id):

    world.server_id = server_id
    world.req = api_utils.retrieve_subscription(tenant_id=world.tenant_id, server_id=world.server_id,
                                                subscription_id=Utils.id_generator(10), headers=world.headers)
