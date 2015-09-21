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
from circus import get_arbiter
import subprocess


class environment_controller():
    """This class provides a control over circus launching.
    """

    started = False

    def check_python_process(self):
        p = subprocess.Popen(['ps', '-awx'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if 'environmentManager.py' in line:
                self.started = True

        return self.started

    def start_manager(self):
        if settings.SETTINGS_TYPE == 'production':
            arbiter = get_arbiter([{"cmd": "python "
                                       "" + settings.ENVIRONMENTS_MANAGER_PATH, "numprocesses": 1}], background=True)

            if not self.check_python_process():
                arbiter.start()

    def is_started(self):
        return self.started
