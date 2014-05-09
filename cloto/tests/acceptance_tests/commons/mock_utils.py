__author__ = 'arobres'


from configuration import MOCK_PORT, MOCK_IP
from constants import MOCK_NOTIFICATION, MOCK_RESET_ERRORS, MOCK_RESET_STATS, MOCK_RESPONSE_SAVE, MOCK_SCALE_DOWN, \
    MOCK_SCALE_UP, MOCK_STATS
import ujson

URL_ROOT = 'http://{}:{}'.format(MOCK_IP, MOCK_PORT)
URL_STATISTICS = URL_ROOT+MOCK_STATS
URL_RESET_STATISTICS = URL_ROOT+MOCK_RESET_STATS
URL_POST_NOTIFICATION = URL_ROOT+MOCK_NOTIFICATION
URL_POST_SCALE_UP = URL_ROOT+MOCK_SCALE_UP
URL_POST_SCALE_DOWN = URL_ROOT+MOCK_SCALE_DOWN
URL_SAVE_RESPONSE = URL_ROOT+MOCK_RESPONSE_SAVE
URL_RESET_RESPONSES = URL_ROOT+MOCK_RESET_ERRORS

import requests


def get_statistics():

    try:

        response = requests.get(URL_STATISTICS)
        response = response.json()

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_STATISTICS, str(e))
            return None

    return response


def reset_statistics():

    try:
        requests.get(URL_RESET_STATISTICS)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_RESET_STATISTICS, str(e))
            return None


def post_notification():

    try:
        requests.post(URL_POST_NOTIFICATION)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_POST_NOTIFICATION, str(e))
            return None


def post_scale_up():

    try:
        requests.post(URL_POST_SCALE_UP)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_POST_SCALE_UP, str(e))
            return None


def post_scale_down():

    try:
        requests.post(URL_POST_SCALE_DOWN)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_POST_SCALE_DOWN, str(e))
            return None


def save_responses(error_code):

    data = ujson.dumps({'error_code': error_code})

    try:
        return requests.post(URL_SAVE_RESPONSE, data)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_POST_SCALE_DOWN, str(e))
            return None


def reset_responses():

    try:
        requests.get(URL_RESET_RESPONSES)

    except Exception, e:
            print "Request {} to {} crashed: {}".format('get', URL_RESET_STATISTICS, str(e))
            return None