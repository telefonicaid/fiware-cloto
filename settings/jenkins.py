__author__ = 'fla'

from os.path import join, exists
from os import makedirs
from cloto.settings import *

# Integrate nose with django. django-nose plugin
INSTALLED_APPS = INSTALLED_APPS + ('django_nose', )

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