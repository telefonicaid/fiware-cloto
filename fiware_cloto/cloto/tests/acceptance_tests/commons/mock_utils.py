#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
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
__author__ = 'arobres'


from commons.configuration import MOCK_PORT, MOCK_IP
from commons.constants import MOCK_NOTIFICATION, MOCK_RESET_ERRORS,\
    MOCK_RESET_STATS, MOCK_RESPONSE_SAVE, MOCK_SCALE_DOWN, \
    MOCK_SCALE_UP, MOCK_STATS
import ujson

URL_ROOT = 'http://{}:{}'.format(MOCK_IP, MOCK_PORT)
URL_STATISTICS = URL_ROOT + MOCK_STATS
URL_RESET_STATISTICS = URL_ROOT + MOCK_RESET_STATS
URL_POST_NOTIFICATION = URL_ROOT + MOCK_NOTIFICATION
URL_POST_SCALE_UP = URL_ROOT + MOCK_SCALE_UP
URL_POST_SCALE_DOWN = URL_ROOT + MOCK_SCALE_DOWN
URL_SAVE_RESPONSE = URL_ROOT + MOCK_RESPONSE_SAVE
URL_RESET_RESPONSES = URL_ROOT + MOCK_RESET_ERRORS

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
