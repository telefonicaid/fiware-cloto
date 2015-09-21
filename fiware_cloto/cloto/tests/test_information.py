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

import datetime

from django.test import TestCase
from fiware_cloto.cloto import information


class InformationTests(TestCase):
    def setUp(self):
        self.body1 = "{\"windowsize\": 4}"
        self.expect1 = 4
        self.body2 = "{\"windowsize\": notValidWindowSize}"
        self.info = information.information("test", "test", "test", datetime.datetime.now(), "test")

    def test_parseInfo(self):
        info = self.info.parse(self.body1)
        self.assertEqual(info.windowsize, self.expect1)

    def test_parseInfo_Error(self):
        info = self.info.parse(self.body2)
        self.assertEqual(info, None)

    def test_get_vars(self):
        result = self.info.getVars()
        self.assertEqual(result, vars(self.info))
