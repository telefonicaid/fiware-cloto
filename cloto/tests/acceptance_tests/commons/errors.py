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

FAULT_ELEMENT_ERROR = u'The {} is not found in the Error Response. The error response obtained is: {}'
ERROR_CODE_ERROR = u'Expected Code is: {} \nObtained Code is: {}'
HTTP_CODE_NOT_OK = u'Invalid HTTP status code. Status Code obtained is: {}\n RESPONSE OBTAINED IS: {}'
INVALID_JSON = u'The JSON received not has the expected content. The content received is: {}'
INCORRECT_SERVER_ID = u'Incorrect ServerId. Expected Server is: {} \nObtained Server is: {}'
