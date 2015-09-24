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
__author__ = 'fla'

from os.path import join, exists
from os import makedirs
from fiware_cloto.cloto_settings.settings import *

# Integrate nose with django. django-nose plugin
INSTALLED_APPS = INSTALLED_APPS + ('django_nose', 'cloto')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# cobertura dir must be in the root of our project not django
COBERTURA_DIR = join('target', 'site', 'cobertura')
UNIT_TESTS_DIR = join('target', 'surefire-reports')

# Create the Cobertura directory if it is not exist
if not exists(COBERTURA_DIR):
    makedirs(COBERTURA_DIR)

# Create the Unit Test directory if it is not exist
if not exists(UNIT_TESTS_DIR):
    makedirs(UNIT_TESTS_DIR)

NOSE_ARGS = ['-s',
             '-v',
             '--cover-erase',
             '--cover-branches',
             '--with-cov',
             '--cover-package=cloto',
             '--cover-xml',
             '--cover-xml-file={0}/coverage.xml'.format(COBERTURA_DIR),
             '--with-xunit',
             '--xunit-file={0}/TEST-nosetests.xml'.format(UNIT_TESTS_DIR)
             ]
