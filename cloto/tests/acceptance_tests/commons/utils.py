__author__ = 'artanis'

from constants import CONTENT_TYPE_HEADER, AUTHENTICATION_HEADER, DEFAULT_CONTENT_TYPE_HEADER



def create_header(content_type=DEFAULT_CONTENT_TYPE_HEADER, token=None):

    header = {CONTENT_TYPE_HEADER: '', AUTHENTICATION_HEADER: ''}

    list_deletions = [None, u'null']
    if content_type in list_deletions:
        del header[CONTENT_TYPE_HEADER]
    else:
        header[CONTENT_TYPE_HEADER] = content_type

    if token in list_deletions:
        del header[AUTHENTICATION_HEADER]
    else:
        header[AUTHENTICATION_HEADER] = token

    return header


def assert_error_code_error(response, expected_error_code=None, expected_fault_element=None,
                            expected_message_error=None):

        assert expected_fault_element in response.keys()
        assert response[expected_fault_element]['code'] == expected_error_code
        assert response[expected_fault_element]['message'] == expected_message_error


