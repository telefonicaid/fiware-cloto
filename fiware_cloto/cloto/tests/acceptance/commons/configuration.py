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


REST_PATH = '../../../../manage.py'
POLICY_MANAGER_IP = 'fiwarecloto'
POLICY_MANAGER_PORT = 8000
FACTS_IP = 'fiwarecloto'
FACTS_PORT = 5000
RABBIT_IP = 'rabbitmq'

AUTH_TOKEN_OLD = ''
KEYSTONE_URL = ''
TENANT_ID = ''
TENANT_NAME = ''
USER = ''
PASSWORD = ''
CONTENT_TYPE = 'application/json'
HEADERS = {'content-type': CONTENT_TYPE, 'X-Auth-Token': ''}
DB_PATH = '../../../../cloto.db'
MOCK_IP = u'127.0.0.1'
MOCK_PORT = 8080
MOCK_PATH = u'commons/server_mock.py'
