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

from ConfigParser import SafeConfigParser
import fiware_cloto as fiware_cloto
import os.path

"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/fiware-cloto.cfg

Optionally, user can specify the file location manually using an Environment variable called CLOTO_SETTINGS_FILE.
"""

name = 'fiware-cloto'

cfg_dir = "/etc/fiware.d"

cfg_defaults_openstack = {
    'OPENSTACK_URL': 'http://cloud.lab.fi-ware.org:4731/v2.0',
    'ADM_USER': '',
    'ADM_PASS': '',
    'ADM_TENANT_ID': '',
    'ADM_TENANT_NAME': '',
    'USER_DOMAIN_NAME': 'Default',
    'AUTH_API': 'v2.0'
}

cfg_defaults_policy_manager = {
    'SECURITY_LEVEL': 'LOW',
    'SETTINGS_TYPE': 'production',
    'DEFAULT_WINDOW_SIZE': 5,
    'MAX_WINDOW_SIZE': 10,
    'LOGGING_PATH': '/var/log/fiware-cloto'
}

cfg_defaults_context_broker = {
    'CONTEXT_BROKER_URL': 'http://130.206.115.92:1026/v1',
    'NOTIFICATION_URL': 'http://127.0.0.1:5000/v1.0',
    'NOTIFICATION_TYPE': 'ONTIMEINTERVAL',
    'NOTIFICATION_TIME': 'PT5S'
}

cfg_defaults_rabbitmq = {
    'RABBITMQ_URL': 'localhost',
}

cfg_defaults_mysql = {
    'DB_CHARSET': 'utf8',
    'DB_HOST': 'localhost',
    'DB_NAME': 'cloto',
    'DB_USER': '',
    'DB_PASSWD': ''
}

cfg_defaults_django = {
    'DEBUG': 'False',
    'DATABASE_ENGINE': 'django.db.backends.mysql',
    'ALLOWED_HOSTS': "['127.0.0.1', 'localhost']",
    'SECRET_KEY': ''
}

cfg_defaults_logging = {
    'level': 'INFO'
}

config = SafeConfigParser()

config.add_section('openstack')
config.add_section('policy_manager')
config.add_section('context_broker')
config.add_section('rabbitmq')
config.add_section('mysql')
config.add_section('django')
config.add_section('logging')

for key, value in cfg_defaults_openstack.items():
    config.set('openstack', key, str(value))

for key, value in cfg_defaults_policy_manager.items():
    config.set('policy_manager', key, str(value))

for key, value in cfg_defaults_context_broker.items():
    config.set('context_broker', key, str(value))

for key, value in cfg_defaults_rabbitmq.items():
    config.set('rabbitmq', key, str(value))

for key, value in cfg_defaults_mysql.items():
    config.set('mysql', key, str(value))

for key, value in cfg_defaults_django.items():
    config.set('django', key, str(value))

for key, value in cfg_defaults_logging.items():
    config.set('logging', key, str(value))

if os.environ.get("CLOTO_SETTINGS_FILE"):
    cfg_filename = os.environ.get("CLOTO_SETTINGS_FILE")
else:
    cfg_filename = os.path.join(cfg_dir, '%s.cfg' % name)

config.read(cfg_filename)


CSRF_FAILURE_VIEW = 'cloto.views.fail'
DEBUG = config.get('django', 'DEBUG')
TEMPLATE_DEBUG = DEBUG
APPEND_SLASH = False

ADMINS = (
    # ('Fernando Lopez', 'fernando.lopezaguilar@telefonica.com'),
    # ('Guillermo Jimenez', 'e.fiware.tid@telefonica.com'),
)

MANAGERS = ADMINS

# OPENSTACK CONFIGURATION
OPENSTACK_URL = config.get('openstack', 'OPENSTACK_URL')
ADM_USER = config.get('openstack', 'ADM_USER')
ADM_PASS = config.get('openstack', 'ADM_PASS')
ADM_TENANT_ID = config.get('openstack', 'ADM_TENANT_ID')
ADM_TENANT_NAME = config.get('openstack', 'ADM_TENANT_NAME')
USER_DOMAIN_NAME = config.get('openstack', 'USER_DOMAIN_NAME')
AUTH_API = config.get('openstack', 'AUTH_API')

# POLICY MANAGER CONFIGURATION
SECURITY_LEVEL = config.get('policy_manager', 'SECURITY_LEVEL')
SETTINGS_TYPE = config.get('policy_manager', 'SETTINGS_TYPE')
INSTALLATION_PATH = os.path.dirname(fiware_cloto.__file__)
ENVIRONMENTS_MANAGER_PATH = INSTALLATION_PATH + u'/environments/environmentManager.py'
ENVIRONMENTS_PATH = INSTALLATION_PATH + u'/environments/environment.py'
RABBITMQ_URL = config.get('rabbitmq', 'RABBITMQ_URL')


DEFAULT_WINDOW_SIZE = config.get('policy_manager', 'DEFAULT_WINDOW_SIZE')
OWNER = u'Telefonica I+D'
API_INFO_URL = u'http://docs.policymanager.apiary.io'
VERSION = u'2.8.0'
MAX_WINDOW_SIZE = config.get('policy_manager', 'MAX_WINDOW_SIZE')
LOGGING_PATH = config.get('policy_manager', 'LOGGING_PATH')
LOGGING_LEVEL = config.get('logging', 'level')


# ORION CONTEXT BROKER CONFIGURATION
CONTEXT_BROKER_URL = config.get('context_broker', 'CONTEXT_BROKER_URL')
NOTIFICATION_URL = config.get('context_broker', 'NOTIFICATION_URL')
NOTIFICATION_TYPE = config.get('context_broker', 'NOTIFICATION_TYPE')
NOTIFICATION_TIME = config.get('context_broker', 'NOTIFICATION_TIME')

# MYSQL CONFIGURATION
DB_CHARSET = config.get('mysql', 'DB_CHARSET')
DB_HOST = config.get('mysql', 'DB_HOST')
DB_NAME = config.get('mysql', 'DB_NAME')
DB_USER = config.get('mysql', 'DB_USER')
DB_PASSWD = config.get('mysql', 'DB_PASSWD')

DATABASES = {
    'default': {
        'ENGINE': config.get('django', 'DATABASE_ENGINE'),  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWD,
        'HOST': DB_HOST,
        'CHARSET': DB_CHARSET
    }
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/cloto_settings/#allowed-hosts
ALLOWED_HOSTS = config.get('django', 'ALLOWED_HOSTS')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('django', 'SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fiware_cloto.cloto.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fiware_cloto.cloto.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fiware_cloto.cloto',
    'fiware_cloto.orion_wrapper',
    'fiware_cloto.environments',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'file_formatter': {
            'format': '%(asctime)s %(levelname)s policymanager.cloto [-] %(message)s'
        },
    },
    'handlers': {
        'my_file': {
            'level': '' + config.get('logging', 'level'),
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': LOGGING_PATH + '/RuleEngine.log',
            'formatter': 'file_formatter'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'file_formatter'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'RuleEngine': {
            'level': '' + config.get('logging', 'level'),
            'handlers': ['my_file'],
            'propagate': False,

        }
    }
}

SECURITY_LEVEL_SECONDS_V3 = {
    'HIGH': '0',
    'MEDIUM': '1800',
    'LOW': '3600'
}

SECURITY_LEVEL_SECONDS_V2 = {
    'HIGH': '0',
    'MEDIUM': '21600',
    'LOW': '84600'
}
