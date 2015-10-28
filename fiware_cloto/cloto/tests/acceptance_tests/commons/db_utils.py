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
import sqlite3
import os

from configuration import DB_PATH
from commons.constants import DB_RULE_AND_SUBSCRIPTION


class DBUtils(object):

    data = None
    tables = []

    def __init__(self):

        assert os.path.exists(DB_PATH)
        print os.path.abspath(DB_PATH)
        try:
            print DB_PATH
            self.connection = sqlite3.connect(DB_PATH)
            self.cursor = self.connection.cursor()

        except:
            print 'Error in the DB access'

        print "DB Utils library initialized"

    def get_all_tables(self):

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables_tmp = self.cursor.fetchall()
        for table_tuple in self.tables_tmp:
            self.tables.append(table_tuple[0])

        return self.tables

    def select_all_elements_table(self, table):

        self.cursor.execute("SELECT * FROM {}".format(table))
        self.data = self.cursor.fetchall()
        return self.data

    def delete_all_element_table(self, table):

        self.cursor.execute("DELETE FROM {}".format(table))

    def delete_rule_and_subscription_tables(self):

        for table in DB_RULE_AND_SUBSCRIPTION:
            self.cursor.execute("DELETE FROM {}".format(table))
            self.connection.commit()

    def close_connection(self):

        self.connection.close()
