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
# Django settings for fiware_cloto project.
CSRF_FAILURE_VIEW = 'cloto.views.fail'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
APPEND_SLASH = False

ADMINS = (
    # ('Fernando Lopez', 'fernando.lopezaguilar@telefonica.com'),
    # ('Guillermo Jimenez', 'e.fiware.tid@telefonica.com'),
)

MANAGERS = ADMINS

# OPENSTACK CONFIGURATION
OPENSTACK_URL = ''
ADM_USER = ''
ADM_PASS = ''
ADM_TENANT_ID = ''
ADM_TENANT_NAME = ''
USER_DOMAIN_NAME = ''
AUTH_API = 'v2.0'

# POLICY MANAGER CONFIGURATION
SETTINGS_TYPE = u'production'
INSTALLATION_PATH = u'/opt/policyManager/fiware-cloto/'
DEFAULT_WINDOW_SIZE = 5
OWNER = u'Telefonica I+D'
API_INFO_URL = u'https://forge.fi-ware.org/plugins/mediawiki/wiki/fiware/index.php/' \
               u'Policy_Manager_Open_RESTful_API_Specification'
VERSION = u'1.5.0'
MAX_WINDOW_SIZE = 5
LOGGING_PATH = u'/var/log/fiware-cloto'

ENVIRONMENTS_MANAGER_PATH = INSTALLATION_PATH + u'environments/environmentManager.py'
ENVIRONMENTS_PATH = INSTALLATION_PATH + u'environments/environment.py'

# ORION CONTEXT BROKER CONFIGURATION
CONTEXT_BROKER_URL = u'http://130.206.82.11:1026/NGSI10'
NOTIFICATION_URL = u'http://130.206.81.71:5000/v1.0'
NOTIFICATION_TYPE = u'ONTIMEINTERVAL'
NOTIFICATION_TIME = u'PT5S'

# MYSQL CONFIGURATION
DB_CHARSET = u'utf8'
DB_HOST = u'localhost'
DB_NAME = u'cloto'
DB_USER = u''
DB_PASSWD = u''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'OPTIONS': {
            'read_default_file': INSTALLATION_PATH + 'settings/db.cfg'
        },
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1']

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
SECRET_KEY = ''

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

ROOT_URLCONF = 'cloto.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cloto.wsgi.application'

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
    'cloto',
    'orion_wrapper',
    'environments',
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
            'level': 'DEBUG',
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
            'level': 'DEBUG',
            'handlers': ['my_file'],
            'propagate': False,

        }
    }
}
