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
"""
WSGI config for fiware_cloto project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "cloto.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloto.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

#import sqlite3
import MySQLdb as mysql
import datetime

from django.utils import timezone
from circus import get_arbiter

from cloto.models import ServerInfo
from cloto.configuration import OWNER, API_INFO_URL, VERSION, ENVIRONMENTS_MANAGER_PATH, INSTALLATION_PATH, \
    DB_NAME, DB_CHARSET, DB_PASSWD, DB_USER, DB_HOST
from cloto.log import logger


#conn = sqlite3.connect(INSTALLATION_PATH + 'cloto.db')
conn = mysql.connect(charset=DB_CHARSET, use_unicode=True, host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

c = conn.cursor()
runningfrom = datetime.datetime.now(tz=timezone.get_default_timezone())
# Creating initial data
try:
    s = ServerInfo(id=1, owner=OWNER, version=VERSION, runningfrom=runningfrom, doc=API_INFO_URL)
    s.save()
except Exception as err:
    logger.warn("DataBase already exists: %s" % err)

# Save (commit) the changes.
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

arbiter = get_arbiter([{"cmd": "python " + ENVIRONMENTS_MANAGER_PATH, "numprocesses": 1}], background=True)
arbiter.start()
logger.info("SERVER STARTED")
