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

import pika

import ujson
from commons.configuration import RABBIT_IP


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
