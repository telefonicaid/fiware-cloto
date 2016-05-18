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
from commons.rest_utils import RestUtils
from commons.constants import TENANT_DOC, TENANT_OWNER, TENANT_VERSION, TENANT_WSIZE, TENANT_DEFAULT_DOC
from commons.configuration import HEADERS, TENANT_ID
import commons.utils as Utils

api_utils = RestUtils()
behave.use_step_matcher("re")


@step(u'the tenant "([^"]*)"')
def set_tenant_id(context, tenant_id):

    context.tenant_id = tenant_id


@step(u'a created tenant')
def set_default_tenant(context):

    #Set default tenant_id as a global variable
    context.tenant_id = TENANT_ID


@step(u'I retrieve the tenant information')
def retrieve_tenant_information(context):

    context.req = api_utils.retrieve_information(tenant_id=context.tenant_id, headers=context.headers)


@step(u'I get the following information')
def check_tenant_information(context):

    assert context.req.ok, 'Invalid HTTP status code. Status Code obtained is: {}'.format(context.req.status_code)

    response = Utils.assert_json_format(context.req)

    for expected_result in context.table.rows:

        assert response[TENANT_DOC] == TENANT_DEFAULT_DOC, 'Expected {} is: {} \n Obtained {} is: ' \
                                                           '{}'.format(TENANT_DOC, TENANT_DEFAULT_DOC,
                                                           TENANT_DOC, response[TENANT_DOC])

        assert response[TENANT_OWNER] == expected_result[TENANT_OWNER], 'Expected {} is: {} \n Obtained {} is: ' \
                                                                        '{}'.format(TENANT_OWNER,
                                                                                    expected_result[TENANT_OWNER],
                                                                                    TENANT_OWNER,
                                                                                    response[TENANT_OWNER])
        assert TENANT_VERSION in response, 'API Version not found in the response'
        assert TENANT_WSIZE in response, 'WindowSize value not found in the API response'


@step(u'I obtain an "([^"]*)" and the "([^"]*)"')
def assert_error_response(context, error_code, fault_element):

    Utils.assert_error_code_error(response=context.req, expected_error_code=error_code,
                                  expected_fault_element=fault_element)


@step(u'an incorrect token with value "([^"]*)"')
def set_incorrect_token(context, token):

    #Set and incorrect header to obtain unauthorized error
    context.headers = Utils.create_header(token=token)


@step(u'I update the window size to "(?P<window_size>.*)"')
def update_window_size(context, window_size):

    try:
        context.window_size = int(window_size)
    except ValueError:
        print("Window Size can not be converted to integer")
        context.window_size = window_size

    context.req = api_utils.update_window_size(tenant_id=context.tenant_id, window_size=context.window_size,
                                               headers=context.headers)


@step(u'the window size is updated in Policy Manager with value "([^"]*)"')
def assert_window_size(context, window_size):

    assert context.req.ok, str(context.req.status_code) + context.req.content

    response = Utils.assert_json_format(context.req)

    assert str(response[TENANT_WSIZE]) == window_size
    context.req = api_utils.retrieve_information(tenant_id=context.tenant_id, headers=context.headers)

    response = Utils.assert_json_format(context.req)

    assert str(response[TENANT_WSIZE]) == window_size
