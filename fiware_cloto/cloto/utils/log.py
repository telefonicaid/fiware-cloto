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
from django.conf import settings
import logging

logger = logging.getLogger('Cloto')
logger.setLevel(settings.LOGGING_LEVEL)
fh = logging.FileHandler(settings.LOGGING_PATH + '/RuleEngine.log')
fh.setLevel(settings.LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s %(levelname)s policymanager.cloto [-] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
