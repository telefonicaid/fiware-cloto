__author__ = 'artanis'
import sqlite3
from configuration import DB_PATH
from constants import DB_RULE_AND_SUBSCRIPTION


class DBUtils(object):

    data = None
    tables = []

    def __init__(self):

        try:
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
