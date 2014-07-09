__author__ = 'arobres'

import pika
import ujson
from configuration import RABBIT_IP


class Rabbit_Utils(object):

    def __init__(self):

        self.queue_name = None
        self.channel = self.start_rabbit_connection()
        self.declare_exchange_and_queue()

    @staticmethod
    def start_rabbit_connection():
        """ Method to start the Rabbit Connection using pika
        :returns channel
        """

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_IP))
        return connection.channel()

    def declare_exchange_and_queue(self, exchange_id='update_tenantid'):

        """ Method to connect the connection to the according exchange
        :param exchange_id: exchange unique identifier
        """

        self.channel.exchange_declare(exchange=exchange_id, type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='update_tenantid', queue=self.queue_name)

    def get_parameters(self):

        """Method to returns one message
        :returns message: JSON with the parameters to update in Policy Manager (string)
        """
        message = self.channel.basic_get(queue=self.queue_name, no_ack=True)
        print message
        return message[2]

    @staticmethod
    def parse_message(message):

        """Method to obtain the parameters cpu, mem and server_id from the string
        :param message: message to parse (string)
        """

        first_position = message.find('{')
        message_filtered = message[first_position:]
        message_dict = ujson.loads(message_filtered)
        cpu = message_dict['cpu']
        mem = message_dict['mem']
        server_id = message_dict['serverId']
        return server_id, cpu, mem
