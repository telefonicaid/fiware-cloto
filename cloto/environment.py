__author__ = 'Geon'
import sys
import pika
import sqlite3 as lite
import logging
from configuration import LOGGING_PATH
logger = logging.getLogger('environments')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGGING_PATH + '/%s.log' % sys.argv[1])
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def main():
    while (True):
        try:
            tenantId = sys.argv[1]

            connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host='localhost'))
            channel = connection.channel()

            channel.exchange_declare(exchange="update_" + tenantId,
                                     type='fanout')

            result = channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange="update_" + tenantId,
                               queue=queue_name)

            logger.info(' [*] Environment started. Waiting for Facts')

            def callback(ch, method, properties, body):
                logger.info(" [x] %r" % (body,))

            channel.basic_consume(callback,
                                  queue=queue_name,
                                  no_ack=True)

            channel.start_consuming()
        except lite.Error, e:
            logger.error("Error %s:" % e.args[0])
        except Exception as ex:
            if ex.message:
                logger.error("Error: %s" % ex.message)
        finally:
            connection.close()

if __name__ == '__main__':
    main()
