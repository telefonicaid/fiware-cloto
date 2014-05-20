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

from subprocess import Popen, PIPE
from time import sleep
from commons.configuration import REST_PATH, REST_PORT, MOCK_PORT, MOCK_PATH
from commons.constants import LITTLE_SLEEP
import requests


class EnvironmentUtils(object):

    def __init__(self):

        self.proc_policy_manager = None
        self.proc_mock = None

    def start_policy_manager(self):

        self.proc_policy_manager = Popen(['python', REST_PATH, REST_PORT])
        sleep(LITTLE_SLEEP)

    def stop_policy_manager(self):

        if self.proc_policy_manager is not None:

            try:
                self.proc_policy_manager.terminate()
                sleep(LITTLE_SLEEP)
                if self.proc_policy_manager.wait() != 0:
                    self.proc_policy_manager.kill()
                self.proc_policy_manager = None

            except OSError:
                pass

        else:
            print 'Police Manager is not running'

    def police_manager_is_up(self):

        #There are two possibilities to know if the police manager is up. The first is using the process using the
        #Django port. Another option can be doing a requests to the server and checking the response. In my opinion the
        #better option is the second.

        pass

    def mock_is_up(self):
        """Method to verify if the HTTP is up, doing a request to the mock"""

        try:
            response = requests.get('http://localhost:{}/stats/'.format(MOCK_PORT))
        except Exception, e:
            print "HTTP mock is not Running"
            return False
        if response.ok:
            print "HTTP mock is UP"
            return True
        else:
            print "HTTP mock is not Running"
            return False

    def start_mock(self):

        """Initialize the HTTP mock in new process. The process is saved in the class to stop it when is required"""

        if not (self.mock_is_up()):
            self.proc_mock = Popen(['python2.7', MOCK_PATH])
            print '------  Starting HTTP Mock ------'

    def stop_mock(self):

        """Stop the HTTP mock. Kills all the processes that are using the TCP port required to the mock"""

        if self.mock_is_up():

            if self.proc_mock:
                try:
                    self.proc_mock.terminate()
                    if self.proc_mock.wait() != 0:
                        self.proc_mock.kill()
                        self.proc_mock = None

                except OSError:
                    pass

            else:
                pid = self.find_process(MOCK_PORT)
                if pid:
                    self.kill_process(pid)

    def find_process(self, port):

        """Method to find the process PID for given TCP port
        :param port: Port number used by the process
        :returns: PID of the process whose use this port, or None if no port are using it.
        """

        port = str(port)
        p1 = Popen(['lsof', '-i', 'tcp:{}'.format(port)], stdout=PIPE)
        p2 = Popen(['awk', ' {print $2}'], stdin=p1.stdout, stdout=PIPE)
        data = p2.communicate()[0].split('\n')
        if len(data) <= 1:
            return None
        else:
            return data[1]

    def kill_process(self, pid):

        """Method to kill the given process"""

        Popen(['kill', '-9', pid])
