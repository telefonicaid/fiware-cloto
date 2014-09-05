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

"""File with Constants used in fiware-cloto proyect.
"""

#HTTP CONTANTS
CONTENT_HEADER = u'Content-Type'
ACCEPT_HEADER = u'Accept'
JSON_TYPE = u'application/json'

#MODEL CONSTANTS
SERVERID = u'serverId'

# NOTIFICATION CONSTANS
OPERATIONS = ["scaleUp", "scaleDown"]
OPERANDS = ["greater", "less", "greater equal", "less equal"]

#MODELS LENGTH
ID_LENGTH = 40
TEXT_LENGTH = 21844
DOC_LENGTH = 3000
URL_LENGTH = 140
NAME_LENGTH = 40
