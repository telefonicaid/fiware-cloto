#!/bin/sh
# File to execute fiware-cloto component
#
# __author__ = 'gjp'

OS=`uname`
IP=`ping -c 1 $HOSTNAME | grep 'PING' | awk '{print $3}' | sed 's/[:()]//g'`;

cd /opt/policyManager/fiware-cloto
python manage.py runserver $IP:8000

