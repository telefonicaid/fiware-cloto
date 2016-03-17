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
# Django cloto_settings for fiware_cloto project.
from cloto_settings.settings import *

SETTINGS_TYPE = u'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': INSTALLATION_PATH + '/cloto.db',                      # Or path to database file if using sqlite3.
        # The following cloto_settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'TestingKey+faeogfjksrjgpjaspigjiopsjgvopjsopgvj'

NOSE_ARGS = [
        '--with-coverage',  # activate coverage report
        '--verbosity=2',   # verbose output
        '--with-xunit',    # enable XUnit plugin
        '--xunit-file=target/surefire-reports/TEST-nosetests.xml',  # the XUnit report file
        '--cover-xml',     # produle XML coverage info
        '--cover-xml-file=target/site/cobertura/coverage.xml',  # the coverage info file
        # You may also specify the packages to be covered here
        '--cover-package=fiware_cloto.cloto,fiware_cloto.orion_wrapper,fiware_cloto.environments'
    ]
