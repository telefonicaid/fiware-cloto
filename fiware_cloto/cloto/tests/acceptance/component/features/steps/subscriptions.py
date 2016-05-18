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
from commons.constants import RULE_ID, SERVER_ID, SUBSCRIPTION_ID, RANDOM, DEFAULT, RULE_URL_DEFAULT, \
    ITEM_NOT_FOUND_ERROR, RULE_URL
from commons.configuration import HEADERS, TENANT_ID
from commons.errors import HTTP_CODE_NOT_OK
import commons.utils as Utils
import commons.rule_utils as Rule_Utils

api_utils = RestUtils()
behave.use_step_matcher("re")


@step(u'a created rule in the "([^"]*)"')
def created_rule(context, server_id):

    context.server_id = server_id
    context.rule_body = Rule_Utils.create_scale_specific_rule()

    # Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=context.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    # Save the Rule ID to obtain the Rule information after
    context.rule_id = req.json()[RULE_ID]


@step(u'I create a new subscription in "([^"]*)" with "([^"]*)"')
def new_subscription_in_server(context, server_id, url_to_notify):

    context.url_to_notify = url_to_notify
    if server_id == RANDOM:
        context.server_id = Utils.id_generator(10)
    else:
        context.server_id = server_id

    context.req = api_utils.create_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                rule_id=context.rule_id, url=context.url_to_notify,
                                                headers=context.headers)


@step(u'I create the same subscription')
def create_subscription_created_before(context):

    context.req = api_utils.create_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                rule_id=context.rule_id, url=context.url_to_notify,
                                                headers=context.headers)


@step(u'the subscription is created')
def assert_subscription_created(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))
    response = Utils.assert_json_format(context.req)
    assert_equals(response[SERVER_ID], context.server_id)
    assert_in(SUBSCRIPTION_ID, response.keys())


@step(u'I obtain an "([^"]*)" and the "([^"]*)"')
def assert_error_response(context, error_code, fault_element):

    Utils.assert_error_code_error(response=context.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'the rule "([^"]*)"')
def given_the_rule(context, rule_id):

    context.tenant_id = TENANT_ID
    context.rule_id = rule_id


@step(u'incorrect "([^"]*)"')
def set_incorrect_token(context, token):
    # Set and incorrect header to obtain unauthorized error
    context.headers = Utils.create_header(token=token)


@step(u'a subscription created in "([^"]*)"')
def created_subscription(context, server_id):

    context.tenant_id = TENANT_ID
    context.server_id = server_id
    context.headers = HEADERS

    context.rule_body = Rule_Utils.create_scale_specific_rule()

    # Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id=context.tenant_id, server_id=context.server_id, body=context.rule_body)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))

    # Save the Rule ID to obtain the Rule information after
    context.rule_id = req.json()[RULE_ID]

    req = api_utils.create_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                        rule_id=context.rule_id, url=RULE_URL_DEFAULT, headers=context.headers)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code, req.content))
    print(req.content)
    context.subscription_id = req.json()[SUBSCRIPTION_ID]


@step(u'I delete a subscription in "([^"]*)"')
def delete_subscription_in_server(context, server_id):

    if server_id == RANDOM:
        context.server_id = Utils.id_generator(10)
    else:
        context.server_id = server_id

    context.req = api_utils.delete_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                subscription_id=context.subscription_id, headers=context.headers)


@step(u'the subscription is deleted')
def assert_subscription_is_deleted(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))
    req = api_utils.retrieve_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                          subscription_id=context.subscription_id, headers=context.headers)
    Utils.assert_error_code_error(response=req, expected_error_code='404',
                                  expected_fault_element=ITEM_NOT_FOUND_ERROR)


@step(u'I delete a not existent subscription in "([^"]*)"')
def delete_non_existent_subscription(context, server_id):

    context.server_id = server_id
    context.req = api_utils.delete_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                subscription_id=Utils.id_generator(10), headers=context.headers)


@step(u'I retrieve the subscription in "([^"]*)"')
def retrieve_subscription(context, server_id):

    if server_id == RANDOM:
        context.server_id = Utils.id_generator(10)
    else:
        context.server_id = server_id

    context.req = api_utils.retrieve_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                  subscription_id=context.subscription_id, headers=context.headers)


@step(u'I get all subscription information')
def assert_subscription_information(context):

    assert_true(context.req.ok, HTTP_CODE_NOT_OK.format(context.req.status_code, context.req.content))
    response = Utils.assert_json_format(context.req)
    assert_equals(response[RULE_URL], RULE_URL_DEFAULT)
    assert_equals(response[SERVER_ID], context.server_id)
    assert_equals(response[SUBSCRIPTION_ID], context.subscription_id)
    assert_equals(response[RULE_ID], context.rule_id)


@step(u'I retrieve a not existent subscription in "([^"]*)"')
def retrieve_non_existent_subscription(context, server_id):

    context.server_id = server_id
    context.req = api_utils.retrieve_subscription(tenant_id=context.tenant_id, server_id=context.server_id,
                                                  subscription_id=Utils.id_generator(10), headers=context.headers)
