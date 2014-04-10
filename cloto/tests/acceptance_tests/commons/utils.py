__author__ = 'artanis'

from constants import CONTENT_TYPE_HEADER, AUTHENTICATION_HEADER, DEFAULT_CONTENT_TYPE_HEADER, RULE_ACTION, \
    RULE_CONDITION, RULE_NAME, RULE_CONDITION_DEFAULT, RULE_ACTION_DEFAULT, LONG_NAME, RULE_ID, RULE_SPECIFIC_ID
from constants import ATTRIBUTES_NAME, ATTRIBUTES_TYPE, ATTRIBUTES_VALUE, ATTRIBUTES_LIST, ATTRIBUTE_PROBE, ATTRIBUTES
from constants import CONTEXT_IS_PATTERN, CONTEXT_IS_PATTERN_VALUE, CONTEXT_SERVER, \
    CONTEXT_SERVER_ID, CONTEXT_TYPE, CONTEXT_ELEMENT, SERVERS, RULES, SERVER_ID, RULE_URL_DEFAULT
from constants import CONTEXT_STATUS_CODE_CODE, CONTEXT_STATUS_CODE_DETAILS, CONTEXT_STATUS_CODE_OK, \
    CONTEXT_STATUS_CODE_REASON, CONTEXT_STATUS_CODE, ORIGINATOR, CONTEXT_RESPONSES, SUBSCRIPTION_ID
from constants import RULE_ACTION_NAME_LIST, RULE_ACTION_NAME
from errors import FAULT_ELEMENT_ERROR, ERROR_CODE_ERROR, HTTP_CODE_NOT_OK
from configuration import TENANT_ID, HEADERS
from rest_utils import RestUtils
from nose.tools import assert_in, assert_equals, assert_true
import string
import random

list_deletions = [None, u'null']


def create_header(content_type=DEFAULT_CONTENT_TYPE_HEADER, token=None):

    """Method to create the header required to perform requests to the Policy Manager
    :param content_type:  Content type of the HTTP request. By default application/json
    :param token: Token required to policy manager authentication
    :returns: HTTP header (dict)
    """

    header = {CONTENT_TYPE_HEADER: '', AUTHENTICATION_HEADER: ''}

    if content_type in list_deletions:
        del header[CONTENT_TYPE_HEADER]
    else:
        header[CONTENT_TYPE_HEADER] = content_type

    if token in list_deletions:
        del header[AUTHENTICATION_HEADER]
    else:
        header[AUTHENTICATION_HEADER] = token

    return header


def assert_error_code_error(response, expected_error_code=None, expected_fault_element=None):

    """Method to assert response errors from Policy Manger
    :param response: Response obtained from the API REST request to the Policy Manager
    :param expected_fault_element: Expected Fault element in the JSON response
    :param expected_error_code: Expected Error code in the JSON response
    """

    assert_equals(expected_error_code, str(response.status_code),
                  ERROR_CODE_ERROR.format(expected_error_code, str(response.status_code)))
    response_body = response.json()
    assert_in(expected_fault_element, response_body.keys(),
              FAULT_ELEMENT_ERROR.format(expected_fault_element, response_body))
    assert_equals(str(response_body[expected_fault_element]['code']), expected_error_code,
                  ERROR_CODE_ERROR.format(expected_error_code, response_body[expected_fault_element]['code']))


def create_rule_parameters(name=None, condition=None, action=None):

    """Method to create the rule body
    :param name: The name of the rule to be created
    :param condition: the condition to compare the server context
    :param action: the action to take over the server
    """

    if name == 'long_name':
        name = LONG_NAME
    elif name == 'None':
        name = None
    elif name == 'random':
        name = id_generator()

    if condition == 'default':
        condition = RULE_CONDITION_DEFAULT
    elif condition == 'None':
        condition = None

    if action == 'default':
        action = RULE_ACTION_DEFAULT
    elif action == 'None':
        action = None

    return name, condition, action


def id_generator(size=10, chars=string.ascii_letters + string.digits):

    """Method to create random ids
    :param size: define the string size
    :param chars: the characters to be use to create the string
    return ''.join(random.choice(chars) for x in range(size))
    """

    return ''.join(random.choice(chars) for x in range(size))


def assert_json_format(request):

    """"Method to assert the JSON format
    :param request: Object with the response
    :return response if is JSON compliance
    """

    try:
        response = request.json()
    except ValueError:
        assert False, "JSON Cannot be decode. Response format not correspond with JSON format"

    return response


def assert_rule_information(response, rule_id, name, condition, action):

    """Method to verify the rule body parameters
    :param response: Response body received from server
    :param rule_id: The expected rule identification number
    :param name: The expected rule name
    :param condition: The expected rule condition
    :param action: The expected rule action
    """

    assert_equals(response[RULE_NAME], name)
    assert_equals(response[RULE_CONDITION], condition)
    assert_equals(response[RULE_ACTION], action)
    assert_equals(response[RULE_ID], rule_id)


def create_rule_body(action=None, rule_id=None, condition=None, name=None):

    """Method to build the Rule JSON including rule_is

    :param rule_id: The expected rule identification number
    :param name: The expected rule name
    :param condition: The expected rule condition
    :param action: The expected rule action
    :returns: rule JSON (dict)
    """

    rule_body = {RULE_ACTION: action,
                 RULE_SPECIFIC_ID: rule_id,
                 RULE_CONDITION: condition,
                 RULE_NAME: name
                 }

    if action is None:
        del rule_body[RULE_ACTION]
    if rule_id is None:
        del rule_body[RULE_ID]
    if condition is None:
        del rule_body[RULE_CONDITION]
    if name is None:
        del rule_body[RULE_NAME]

    return rule_body


def context_element(cpu_value=None, memory_value=None, disk_value=None, network_value=None, server_id=None):

    """Method to create one context server body
    :param cpu_value: current value of the CPU
    :param memory_value: current value of the RAM memory
    :param disk_value: current value of the HDD
    :param network_value: current value of the network
    :param server_id: Server unique identifier
    :returns context_server_body:
    """

    context_attributes_body = []
    attribute_values = [cpu_value, memory_value, disk_value, network_value]
    for name, value in zip(ATTRIBUTES_LIST, attribute_values):

        if value is None:
            pass
        elif value == 'None':
            pass
        else:
            context_attributes_body.append({ATTRIBUTES_NAME: name, ATTRIBUTES_TYPE: ATTRIBUTE_PROBE,
                                            ATTRIBUTES_VALUE: value})

    context_element_body = {CONTEXT_TYPE: CONTEXT_SERVER,
                            CONTEXT_IS_PATTERN: CONTEXT_IS_PATTERN_VALUE,
                            CONTEXT_SERVER_ID: server_id,
                            ATTRIBUTES: context_attributes_body}
    return context_element_body


def context_status_code(status_code=None, details='message', reason=CONTEXT_STATUS_CODE_OK):

    """Method to build the status code json
    :param status_code: Numerical status code generated from context server
    :param details: Details regarding the context
    :param reason: Information about the context
    return JSON with status code information (dict)
    """

    status_code_body = {CONTEXT_STATUS_CODE_CODE: status_code,
                        CONTEXT_STATUS_CODE_REASON: reason,
                        CONTEXT_STATUS_CODE_DETAILS: details}

    return status_code_body


def context_response(context_element, status_code):

    """Method to build the JSON wiht the context element and the status code
    :param context_element: JSON including the context element attributes
    :param status_code: status code received from context manager
    """

    return {CONTEXT_ELEMENT: context_element,
            CONTEXT_STATUS_CODE: status_code}


def context_server(context_responses, originator=None, subscription_id=None):

    """Method to create the JSON with all context responses
    :param context_responses: List with all context responses from server
    :param originator: String with the originator identifier
    :param subscription_id: OpenStack subscription unique identifier
    :returns JSON with all context responses.
    """

    return {SUBSCRIPTION_ID: subscription_id,
            ORIGINATOR: originator,
            CONTEXT_RESPONSES: context_responses}


def build_one_context_server(cpu_value=None, memory_value=None, disk_value=None, network_value=None, server_id=None,
                             subscription_id=None):

    """Method to create a context server body with only one measure.
    :param cpu_value: current value of the CPU
    :param memory_value: current value of the RAM memory
    :param disk_value: current value of the HDD
    :param network_value: current value of the network
    :param server_id: Server unique identifier
    :returns context_server_body:
    """
    context_element_body = context_element(cpu_value, memory_value, disk_value, network_value, server_id)
    context_status_code_body = context_status_code(status_code='200')
    context_response_body = []
    context_response_body.append(context_response(context_element_body, context_status_code_body))
    context_server_body = context_server(context_response_body, None, subscription_id)
    return context_server_body


def delete_all_rules_from_tenant(tenant_id=TENANT_ID):

    """Method to delete all rules from a specific tenant
    :param tenant_id: Tenant unique identifier
    """

    api_utils = RestUtils()
    req = api_utils.retrieve_server_list(tenant_id=tenant_id)
    response = req.json()
    for server in response[SERVERS]:
        server_id = server[SERVER_ID]
        for rule_server in server[RULES]:
            api_utils.delete_rule(tenant_id=tenant_id, server_id=server_id, rule_id=rule_server[RULE_SPECIFIC_ID])


def create_rule(api_utils, tenant_id=TENANT_ID, server_id=None, rule_name=None, rule_condition=None, rule_action=None,
                headers=HEADERS):

    """Method to subscribe a server to a specific rule not created.
    :param server_id: Server unique identifier
    :param headers: HTTP headers for the requests including authentication
    :param tenant_id: Tenant unique identifier
    :param rule_name: Name of the rule to be created
    :param rule_condition: Condition of the rule to be created
    :param rule_action: Action of the rule to be created
    :returns subscription_id: Subscription unique identifier
    """

    #Prepare rule parameters
    r_name, r_condition, r_action = create_rule_parameters(rule_name, rule_condition, rule_action)

    #Create the rule in Policy Manager
    req = api_utils.create_rule(tenant_id, server_id, r_name, r_condition, r_action, headers)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code))

    rule_id = req.json()[RULE_ID]
    return rule_id


def create_subscription(api_utils, server_id=None, headers=HEADERS, tenant_id=TENANT_ID, rule_name=None,
                        rule_condition=None, rule_action=None):

    """Method to subscribe a server to a specific rule not created.
    :param server_id: Server unique identifier
    :param headers: HTTP headers for the requests including authentication
    :param tenant_id: Tenant unique identifier
    :param rule_name: Name of the rule to be created
    :param rule_condition: Condition of the rule to be created
    :param rule_action: Action of the rule to be created
    :returns subscription_id: Subscription unique identifier
    """

    rule_id = create_rule(api_utils, tenant_id, server_id, rule_name, rule_condition, rule_action, headers)

    req = api_utils.create_subscription(tenant_id=tenant_id, server_id=server_id,
                                        rule_id=rule_id, url=RULE_URL_DEFAULT, headers=headers)

    assert_true(req.ok, HTTP_CODE_NOT_OK.format(req.status_code))
    subscription_id = req.json()[SUBSCRIPTION_ID]
    return subscription_id


def update_context_constant_parameter(parameter, value, context_body):

    """Method to update a parameter inside context JSON
    :param parameter: Parameter to delete
    :param context_body: JSON with all the context body
    :returns Context Body JSON without the parameter updated (dict)
    """

    if parameter == 'isPattern':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_IS_PATTERN] = value
    elif parameter == 'server_type':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_TYPE] = value
    elif parameter == 'name':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_NAME] = value
    elif parameter == 'at_type':
        context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_TYPE] = value

    return context_body


def delete_context_constant_parameter(parameter, context_body):

    """Method to delete a parameter inside context JSON
    :param parameter: Parameter to delete
    :param context_body: JSON with all the context body
    :returns Context Body JSON without the parameter deleted (dict)
    """

    if parameter == 'isPattern':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_IS_PATTERN])
    elif parameter == 'server_type':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][CONTEXT_TYPE])
    elif parameter == 'name':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_NAME])
    elif parameter == 'at_type':
        del(context_body[CONTEXT_RESPONSES][0][CONTEXT_ELEMENT][ATTRIBUTES][random.randint(0, 3)][ATTRIBUTES_TYPE])

    return context_body


def new_create_rule_action_dict(action_name=None, operation=None, body=None, email=None):

    action = {}

    if action_name is not None:
        action[RULE_ACTION_NAME] = action_name

    if operation is not None:
        action['operation'] = operation

    if body is not None:
        action['description'] = body

    if email is not None:
        action['email'] = email

    return action


def new_create_rule_parameter_dict(value=None, operand=None):

    tmp_dict = {}

    if value is not None:
        tmp_dict['value'] = value

    if operand is not None:
        tmp_dict['operation'] = operand

    return tmp_dict


def delete_keys_from_dict(dict_del, key):

    if key in dict_del.keys():

        del dict_del[key]
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, key)

    return dict_del


def replace_values_from_dict(dict_replace, key, replace_to=None):

    if key in dict_replace.keys():

        dict_replace[key] = replace_to
    for v in dict_replace.values():
        if isinstance(v, dict):
            replace_values_from_dict(v, key)

    return dict_replace
