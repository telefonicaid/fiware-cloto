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
__author__ = 'gjp'


# OPENSTACK CONFIGURATION
OPENSTACK_URL = u''
ADM_USER = u''
ADM_PASS = u''
ADM_TENANT_ID = u''

# POLICY MANAGER CONFIGURATION
INSTALLATION_PATH = u'/opt/policyManager/fiware-cloto/'
DEFAULT_WINDOW_SIZE = 5
OWNER = u'Telefonica I+D'
API_INFO_URL = u'https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/' \
               u'index.php/FIWARE.OpenSpecification.Details.Cloud.PolicyManager'
VERSION = 1.0
MAX_WINDOW_SIZE = 10
LOGGING_PATH = u'/var/log/fiware-cloto'
RABBITMQ_URL = u'localhost'

ENVIRONMENTS_MANAGER_PATH = INSTALLATION_PATH + u'cloto/environmentManager.py'
ENVIRONMENTS_PATH = INSTALLATION_PATH + u'cloto/environment.py'
CLIPS_PATH = INSTALLATION_PATH + u'cloto/clips'

# ORION CONTEXT BROKER CONFIGURATION
CONTEXT_BROKER_URL = u'http://130.206.82.11:1026/NGSI10'
NOTIFICATION_URL = u'http://130.206.81.71:5000/v1.0'
NOTIFICATION_TYPE = u'ONTIMEINTERVAL'
NOTIFICATION_TIME = u'PT5S'

# MYSQL CONFIGURATION
DB_CHARSET = u'utf8'
DB_HOST = u'localhost'
DB_NAME = u'cloto'
DB_USER = u''
DB_PASSWD = u''
