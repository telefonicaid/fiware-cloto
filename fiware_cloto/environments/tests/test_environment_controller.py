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
import unittest
from fiware_cloto.environments import environment_controller
from mock import patch, Mock


WITHOUT = """
15009 pts/1    Ss     0:00 -bash
15094 ?        S      0:00 upstart-udev-bridge --daemon
15097 ?        S      0:00 upstart-socket-bridge --daemon
15100 ?        S      0:00 upstart-file-bridge --daemon
44657 ttys000 Ss 0:00.00 grep fiware_cloto/environments
"""

WITH = """
15009 pts/1    Ss     0:00 -bash
15094 ?        S      0:00 upstart-udev-bridge --daemon
15097 ?        S      0:00 upstart-socket-bridge --daemon
15100 ?        S      0:00 upstart-file-bridge --daemon
16424 ?        Ss     0:00 python /usr/lib/python2.7/dist-packages/fiware_cloto/environments/environmentManager.py
44657 ttys000 Ss 0:00.00 grep fiware_cloto/environments

"""


class MockPopen(unittest.TestCase):

    def setUp(self):
        self.popen_patcher = patch('fiware_cloto.environments.environment_controller.Popen')
        self.mock_popen = self.popen_patcher.start()

        self.mock_rv = Mock()
        # communicate() returns [STDOUT, STDERR]
        self.mock_rv.communicate.return_value = [WITHOUT, None]
        self.mock_popen.return_value = self.mock_rv

    # run after each test
    def tearDown(self):
        self.popen_patcher.stop()

    def test_clean_no_environments(self):
        """test_clean_no_environments should check that there are no environments to clean."""
        result = environment_controller.check_python_process()
        self.assertEqual(False, result)

        environment_controller.clean_environments()
        self.assertTrue(self.mock_popen.called)

    def test_clean_one_environments(self):
        """test_clean_environments should create an environment manager and clean the environment."""
        self.mock_rv.communicate.return_value = [WITH, None]
        result = environment_controller.check_python_process()
        self.assertEqual(True, result)
        self.mock_rv.communicate.return_value = [WITHOUT, None]
        environment_controller.clean_environments()
        self.assertTrue(self.mock_popen.called)
        result = environment_controller.check_python_process()
        self.assertEqual(False, result)
