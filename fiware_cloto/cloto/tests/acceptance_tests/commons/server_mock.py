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

from collections import deque

from bottle import run, Bottle, request, response
from configuration import MOCK_IP, MOCK_PORT
from commons.constants import MOCK_NOTIFICATION, MOCK_RESET_ERRORS,\
    MOCK_RESET_STATS, MOCK_RESPONSE_SAVE, MOCK_SCALE_DOWN, \
    MOCK_SCALE_UP, MOCK_STATS, MOCK_NUM_NOTIFICATIONS, MOCK_NUM_SCALE_DOWN, MOCK_NUM_SCALE_UP
import ujson

app = Bottle()
statistics = {MOCK_NUM_SCALE_UP: 0,
              MOCK_NUM_SCALE_DOWN: 0,
              MOCK_NUM_NOTIFICATIONS: 0}

responses_error = deque()


@app.post(MOCK_RESPONSE_SAVE)
def save_response():

    body = "".join(request.body)
    try:
        body = ujson.loads(body)
    except:
        response.status = 400
        return {"message": "The JSON format is not correct"}

    if 'error_code' not in body.keys():
        response.status = 400
        return {"message": "Error code is not included in the request"}
    else:
        responses_error.append(body['error_code'])


@app.get(MOCK_RESET_ERRORS)
def reset_errors():

    responses_error.clear()


@app.post(MOCK_SCALE_UP)
def scale_up():
    if responses_error:
        response.status = int(responses_error.popleft())
        return {"message": "Error response: {}".format(response.status)}
    else:
        statistics['num_scale_up'] += 1


@app.post(MOCK_SCALE_DOWN)
def scale_up():
    statistics['num_scale_down'] += 1


@app.post(MOCK_NOTIFICATION)
def scale_up():
    statistics['num_notifications'] += 1


@app.get(MOCK_RESET_STATS)
def reset_stats():
    for x in statistics.keys():
        statistics[x] = 0


@app.get(MOCK_STATS)
def get_stats():

    return statistics


run(app, host=MOCK_IP, port=MOCK_PORT, reloader=True)
