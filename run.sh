#!/bin/sh
# File to execute fiware-cloto component
#
# __author__ = 'gjp'

OS=`uname`
IP=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`;

cd /opt/policyManager/fiware-cloto
python manage.py runserver $IP:8000

