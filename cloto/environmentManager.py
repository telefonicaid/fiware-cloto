__author__ = 'Geon'
import signal
import time
import sys
import sqlite3 as lite

from circus.process import Process

from configuration import ENVIRONMENTS_PATH
from log import logger


def main():

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
            conn = lite.connect('cloto.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cloto_tenantinfo')
            data = cursor.fetchall()
            if tenants.__len__() < data.__len__():
                for tenant in data:
                    if tenant not in tenants:
                        tenants.append(tenant)
                        id = tenant[0]
                        process = Process('Top', 'python ' + ENVIRONMENTS_PATH + ' %s' % id)
                        logger.info("Starting new environment for %s - pid: " % id)
                        processes.append(process)

        except lite.Error, e:
                logger.error("Error %s:" % e.args[0])
        except Exception, e:
                logger.error("Error %s" % e.message)
        finally:
            if conn:
                conn.close()
            time.sleep(5)

if __name__ == '__main__':
    main()
