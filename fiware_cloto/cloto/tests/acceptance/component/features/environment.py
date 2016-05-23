#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014-2016 Telefónica Investigación y Desarrollo, S.A.U
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
from commons.configuration import HEADERS, TENANT_ID
import commons.authentication as Auth
import commons.utils as Utils


def before_feature(context, feature):
    # Set Token Id of the feature
    token_id, context.tenant_id = Auth.get_token()
    HEADERS['X-Auth-Token'] = token_id


def before_scenario(context, scenario):
    # Set default headers with correct token before every scenario
    context.headers = HEADERS
    Utils.delete_all_rules_from_tenant()
    context.rules = []
