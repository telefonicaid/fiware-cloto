#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
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
from django.test import TestCase

import clips
from fiware_cloto.environments import environment


class ClientTests(TestCase):

    def setUp(self):
        """sets up the environment to work with."""
        id = 'tenantId'
        self.json_fact = '{"serverId": "serverId", "cpu": 90, "mem": 30, "hdd":70, "net":90}'
        clips.Reset()
        self.e1 = clips.Environment()
        eid = clips.Symbol(id)
        self.e1.Identifier = eid

    def test_build_fact(self):
        """test_build_fact should check that environment creates a new fact and this fact is not empty."""
        fact = environment.build_fact(self.e1, self.json_fact)
        self.assertIsNotNone(fact)
        self.assertIsNotNone(self.e1)
