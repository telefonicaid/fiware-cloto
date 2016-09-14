#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014-2016 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FIWARE project.
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

import sys
import os.path
import tempfile
from pip.req import parse_requirements
from setuptools import setup, find_packages
from distutils.command.install import install as _install


# create a temporary config file to hold a fake secret key
temp_cfg = tempfile.NamedTemporaryFile()
os.environ.setdefault('CLOTO_SETTINGS_FILE', temp_cfg.name)
temp_cfg.write('[django]\nSECRET_KEY: secret\n')
temp_cfg.flush()


# get module version from default settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fiware_cloto.cloto_settings.settings')
version = __import__(os.environ['DJANGO_SETTINGS_MODULE'], globals(), locals(), ['VERSION'], -1).VERSION


# parse_requirements() returns a generator of pip.req.InstallRequirement objects
# > install_requires is a list of requirements as ['Django==1.9.4', 'requests==2.6.0']
# > dependency_links is a list of URLs to download packages from
try:
    requirements = parse_requirements("requirements.txt", session=False)
    install_requires, dependency_links = map(lambda ir_tuple: [str(item) for item in ir_tuple if item],
                                             zip(*[(ir.req, ir.link) for ir in requirements]))
except TypeError:
    print "error: please upgrade pip version"
    sys.exit(1)


def _post_install(dir):
    # ensure requirements are installed
    import pip
    pip.main(['install'] + install_requires + dependency_links)

    # import django configuration
    from django.conf import settings

    # create additional required directories
    if not os.path.exists(settings.LOGGING_PATH):
        os.makedirs(settings.LOGGING_PATH)

    # setup database
    import django
    from django.db.utils import OperationalError
    from django.core.management import call_command
    try:
        django.setup()
        call_command('makemigrations', 'cloto', verbosity=3, interactive=False)
        call_command('migrate', verbosity=3, interactive=False)
    except OperationalError:
        print "error: couldn't connect to database '%s' at '%s'" % (settings.DB_NAME, settings.DB_HOST)


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,), msg="Running post install task")
        temp_cfg.close()


setup(
    name='fiware-cloto',
    packages=find_packages(exclude=['*tests*']),
    install_requires=install_requires,
    dependency_links=dependency_links,
    package_data={
        'cloto_settings': ['*.cfg']
    },
    data_files=[
        ('/etc/fiware.d', ['fiware_cloto/cloto_settings/fiware-cloto.cfg'])
    ],
    version=version,
    description='This module is part of FIWARE Policy Manager. It provides a REST API to create rules associated '
                'to servers, subscribe servers to Context Broker to get information about their resources consumption '
                'and launch actions described in rules when conditions are met.',
    author='Fernando Lopez Aguilar, Guillermo Jimenez Prieto',
    author_email='fernando.lopezaguilar@telefonica.com, e.fiware.tid@telefonica.com',
    license='Apache 2.0',
    url='https://github.com/telefonicaid/fiware-cloto',
    download_url='https://github.com/telefonicaid/fiware-cloto/tarball/v%s' % version,
    keywords=['fiware', 'policy', 'manager', 'cloud'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License', ],
    cmdclass={'install': install},
)
