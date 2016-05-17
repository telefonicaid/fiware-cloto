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


LITTLE_SLEEP = 1

#INFORMATION RESPONSE CONSTANTS

TENANT_OWNER = u'owner'
TENANT_WSIZE = u'windowsize'
TENANT_DOC = u'doc'
TENANT_VERSION = u'version'
TENANT_KEY = u'tenantId'
TENANT_DEFAULT_DOC = u'http://docs.policymanager.apiary.io'

CONTENT_TYPE_HEADER = u'content-type'
DEFAULT_CONTENT_TYPE_HEADER = u'application/json'
AUTHENTICATION_HEADER = u'X-Auth-Token'

SERVER_ID = u'serverId'

RULE_NAME = u'name'
RULE_CONDITION = u'condition'
RULE_OPERATION = u'operation'
RULE_ACTION = u'action'
RULE_ID = u'ruleId'
RULE_OPERAND = u'operand'
RULE_VALUE = u'value'
RULE_SPECIFIC_ID = u'specificRule_Id'
RULE_URL = u'url'
RULE_CONDITION_DEFAULT = u'?serv <- (server (server-id ?x) (cpu ?y&:(< ?y 30)) (mem ?z) (hdd ?t))'
RULE_ACTION_DEFAULT = u'assert (alertCPU ?x))(python-call env-call-rest-api)'
RULE_URL_DEFAULT = u'http://localhost:8080/notify'
RULE_ACTION_NAME_LIST = ['notify-scale', 'notify-email']
RULE_ACTION_SCALE_LIST = ['scaleUp', 'scaleDown']
RULE_ACTION_NAME = 'actionName'
OPERANDS = ["greater", "less", "greater equal", "less equal"]
BODY = u'body'
MEM = u'mem'
CPU = u'cpu'
HDD = u'hdd'
NET = u'net'
EMAIL = u'email'
DEFAULT_BODY = "Be careful, the mem is too low!!!!"
LONG_NAME = u'This is a long name to test the maximum length of elasticity rule'

RULES = u'rules'
SERVERS = u'servers'

SUBSCRIPTION_ID = u'subscriptionId'
ORIGINATOR = u'originator'
CONTEXT_RESPONSES = u'contextResponses'

RANDOM = u'random'
DEFAULT = u'default'

ITEM_NOT_FOUND_ERROR = u'itemNotFound'

ATTRIBUTE_PROBE = u'Probe'

#DB_TABLES

DB_SPECIFIC_RULES = u'cloto_specificrule'
DB_SUBSCRIPTION = u'cloto_subscription'
DB_ENTITY_SPECIFIC_RULES = u'cloto_entity_specificrules'
DB_ENTITY_SUBSCRIPTION = u'cloto_entity_subscription'
DB_CLOTO_ENTITY = u'cloto_entity'
DB_RULE_AND_SUBSCRIPTION = (DB_SPECIFIC_RULES, DB_SUBSCRIPTION, DB_ENTITY_SUBSCRIPTION, DB_ENTITY_SPECIFIC_RULES,
                            DB_CLOTO_ENTITY)

ATTRIBUTES_NAME = u'name'
ATTRIBUTES_TYPE = u'type'
ATTRIBUTES_VALUE = u'value'
ATTRIBUTE_STRING = u'string'
ATTRIBUTE_CPU = u'cpuLoadPct'
ATTRIBUTE_MEMORY = u'usedMemPct'
ATTRIBUTE_DISK = u'freeSpacePct'
ATTRIBUTE_NETWORK = u'netLoadPct'
ATTRIBUTES = u'attributes'

ATTRIBUTES_LIST = [ATTRIBUTE_CPU, ATTRIBUTE_MEMORY, ATTRIBUTE_DISK, ATTRIBUTE_NETWORK]

CONTEXT_TYPE = u'type'
CONTEXT_SERVER = u'server'
CONTEXT_IS_PATTERN = u'isPattern'
CONTEXT_IS_PATTERN_VALUE = u'false'
CONTEXT_SERVER_ID = u'id'
CONTEXT_ELEMENT = u'contextElement'

CONTEXT_STATUS_CODE_CODE = u'code'
CONTEXT_STATUS_CODE_OK = u'Ok'
CONTEXT_STATUS_CODE_REASON = u'reasonPhrase'
CONTEXT_STATUS_CODE_DETAILS = u'details'
CONTEXT_STATUS_CODE = u'statusCode'
RESPONSE_OK_CODE = 200

#MOCK PATHS

MOCK_RESPONSE_SAVE = '/save_response/'
MOCK_RESET_ERRORS = '/reset_errors/'
MOCK_SCALE_UP = '/scale_up/'
MOCK_SCALE_DOWN = '/scale_down/'
MOCK_NOTIFICATION = '/notification/'
MOCK_RESET_STATS = '/reset_stats/'
MOCK_STATS = '/stats/'

MOCK_NUM_NOTIFICATIONS = 'num_notifications'
MOCK_NUM_SCALE_UP = 'num_scale_up'
MOCK_NUM_SCALE_DOWN = 'num_scale_down'
