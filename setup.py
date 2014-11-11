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
from distutils.core import setup
from django.conf import settings
setup(
  name='fiware-cloto',
  packages=['fiware-cloto'],  # this must be the same as the name above
  version=settings.VERSION,
  description='This module is part of FI-WARE Policy Manager. It provides an API-REST to create rules associated '
            'to servers, subscribe servers to Context Broker to get information about resources consumption of that'
            ' servers and launch actions described in rules when conditions are given.',
  author='Fernando Lopez Aguilar, Guillermo Jimenez Prieto',
  author_email='fernando.lopezaguilar@telefonica.com, e.fiware.tid@telefonica.com',
  license='Apache 2.0',
  url='https://github.com/telefonicaid/fiware-cloto',
  download_url='https://github.com/telefonicaid/fiware-cloto/tarball/v%s' % settings.VERSION,
  keywords=['fiware', 'policy', 'manager', 'cloud'],
  classifiers=[
        "License :: OSI Approved :: Apache Software License", ],
)
