__author__ = 'artanis'

from constants import CONTENT_TYPE_HEADER, AUTHENTICATION_HEADER, DEFAULT_CONTENT_TYPE_HEADER, RULE_ACTION, \
    RULE_CONDITION, RULE_NAME, RULE_CONDITION_DEFAULT, RULE_ACTION_DEFAULT, LONG_NAME
from errors import FAULT_ELEMENT_ERROR, ERROR_CODE_ERROR
from nose.tools import assert_in, assert_equals
import string, random

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