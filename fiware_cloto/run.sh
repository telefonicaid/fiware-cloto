#!/bin/sh
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
# File to execute fiware-cloto component
#
# __author__ = 'gjp'

localIp=`ifconfig | awk '/^[^ -].*: / {if (match($0,/vbox/)) pr=0;  else pr=1} ; /inet (addr:)?([0-9]*\.){3}[0-9]*/ {if (pr) print $2}' | grep -v '127.0.0.1'`
gunicorn fiware_cloto.cloto.wsgi -b $localIp &
