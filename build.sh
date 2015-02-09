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
# File to execute the covertura and unit test and generate the information
# to be shown in sonar
#
# __author__ = 'fla'

virtualenv ENV
source ENV/bin/activate
mkdir -m 777 /var/log/fiware-cloto
pip install -r requirements.txt

#PYCLIPS installation
wget -O pyclips.tar.gz http://downloads.sourceforge.net/project/pyclips/pyclips/pyclips-1.0/pyclips-1.0.7.348.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpyclips%2Ffiles%2Fpyclips%2Fpyclips-1.0%2F&ts=1423484225&use_mirror=softlayer-ams
sleep 3
tar -xvzf pyclips.tar.gz
cd pyclips
python setup.py build
su -c "python setup.py install"
cd ..

export DJANGO_SETTINGS_MODULE=settings.settings_tests
export SETTINGS_TYPE=test
echo "no" | python manage.py syncdb
coverage run --source=cloto,orion_wrapper,environments manage.py test
coverage xml -o target/site/cobertura/coverage.xml



if [ ! $1 = "travis_build" ];
then
    deactivate
    echo "Deactivate completed"
else
    echo "Travis does not have deactivate command for no reason :SS"
fi
