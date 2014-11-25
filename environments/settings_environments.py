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

# POLICY MANAGER CONFIGURATION
SETTINGS_TYPE = u'production'
INSTALLATION_PATH = u'/opt/policyManager/fiware-cloto/'
LOGGING_PATH = u'/var/log/fiware-cloto'

ENVIRONMENTS_PATH = INSTALLATION_PATH + u'environments/environment.py'

# MYSQL CONFIGURATION
DB_CHARSET = u'utf8'
DB_HOST = u'localhost'
DB_NAME = u'cloto'
DB_USER = u'policymanager'
DB_PASSWD = u'policymanager'

RABBITMQ_URL = u'localhost'
