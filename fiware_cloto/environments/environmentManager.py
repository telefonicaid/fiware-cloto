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
import signal
import time
import sys
import os

import MySQLdb as mysql
from circus.process import Process

from fiware_cloto.cloto_settings.settings import SETTINGS_TYPE, DB_CHARSET, DB_HOST, DB_NAME, \
    DB_PASSWD, DB_USER, INSTALLATION_PATH, ENVIRONMENTS_PATH
from fiware_cloto.environments.log import logger


def main():
    if os.environ.get("SETTINGS_TYPE"):
        execution_type = os.environ.get("SETTINGS_TYPE")
    else:
        execution_type = SETTINGS_TYPE

    tenants = []
    processes = []

    def exit_program(*args):
        for p in processes:
            logger.info("Process finished %s" % p.pid)
            p.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_program)

    while (True):
        try:
            conn = None
            if execution_type == 'production':
                conn = mysql.connect(charset=DB_CHARSET, use_unicode=True, host=DB_HOST,
                                 user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
            elif execution_type == "test":
                import sqlite3 as lite
                conn = lite.connect(INSTALLATION_PATH + 'cloto.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cloto.cloto_tenantinfo')
            data = cursor.fetchall()
            if tenants.__len__() < data.__len__():
                for tenant in data:
                    if tenant not in tenants:
                        tenants.append(tenant)
                        id = tenant[0]
                        process = Process('Top', 'python ' + ENVIRONMENTS_PATH + ' %s' % id)
                        logger.info("Starting new environment for %s - pid: " % id)
                        logger.info(ENVIRONMENTS_PATH)

                        processes.append(process)

        except mysql.Error, e:
                logger.error("Error %s:" % e.args[0])
        except Exception, e:
                logger.error("Error %s" % e.message)
        finally:
            if conn:
                conn.close()
            time.sleep(5)
            if execution_type == "test":
                exit_program()

if __name__ == '__main__':
    main()
