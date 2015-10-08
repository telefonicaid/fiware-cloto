===============================
FIWARE Policy Manager GE: Cloto
===============================


| |Build Status| |Coverage Status| |Pypi Version| |Pypi License|

.. contents:: :local:

Introduction
============

This is the code repository for **FIWARE Policy Manager GE - Cloto**, a server that provides an API-REST to
create rules associated to servers, subscribe servers to Context Broker to get information about resources
consumption of that servers and launch actions described in rules when conditions are given.

This project is part of FIWARE_.
Check also the `FIWARE Catalogue entry for Policy Manager`__

__ `FIWARE Policy Manager - Catalogue`_

Any feedback on this documentation is highly welcome, including bugs, typos or
things you think should be included but aren't. You can use `github issues`__
to provide feedback.

__ `Fiware-cloto - GitHub issues`_

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

GEi overall description
=======================
Bosun GEri is the reference implementation of Policy Manager GE.

Bosun GEri offers decision-making ability, independently of the type of resource (physical/virtual resources,
network, service, etc.)  being able to solve complex problems within the Cloud field by reasoning about the knowledge
base, represented by facts and rules.
Bosun GEri provides the basic management of cloud resources based on rules, as well as management of the corresponding
resources within FIWARE Cloud instances based on infrastructure physical monitoring, resources and services
security monitoring or whatever that could be defined by facts, actions and rules.

The baseline for the Bosun GEri is PyCLIPS, which is a module to interact with CLIPS expert system implemented in
python language. The reason to take PyCLIPS is to extend the OpenStack ecosystem with an expert system, written in
the same language as the rest of the OpenStack services.
Besides, It provides notification service to your own HTTP server where you can define your
own actions based on the notifications launched by Policy Manager.
Last but not least, Bosun is integrated with the Monitoring GEri in order to recover the information of the (virtual)
system and calculate any possible change on it based on the knowledge database defined for it.

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Components
----------

Fiware-Cloto
    Fiware-cloto is part of FIWARE Policy Manager. It provides an API-REST to create rules associated to servers,
    subscribe servers to Context Broker to get information about resources consumption of that servers and launch actions
    described in rules when conditions are given.

Fiware-Facts
    Server to process the incoming facts from the
    `Orion Context Broker <https://github.com/telefonicaid/fiware-orion>`__
    and publish the result into a RabbitMQ queue to be analysed by Fiware-Cloto. The facts are the result of the server
    resources consumption.

For more information, please refer to the `documentation <doc/README.rst>`_.

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Build and Install
=================

Requirements
------------

- Operating systems: CentOS (RedHat) and Ubuntu (Debian), being CentOS 6.3 the
  reference operating system.

To install this module you have to install some components:

- Python 2.7
- PyClips 1.0 (http://sourceforge.net/projects/pyclips/files/)
- RabbitMQ Server 3.3.0 or above (http://www.rabbitmq.com/download.html)
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)
- gcc-c++ and gcc libraries

This module also needs the installation of these other components:

- Fiware-facts module installed (https://github.com/telefonicaid/fiware-facts)
- A running instance of Orion Context Broker (https://github.com/telefonicaid/fiware-orion)
- fiware-monitoring connected to the Orion instance to provide
  information about servers (https://github.com/telefonicaid/fiware-monitoring).

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Installation
------------

Once you have all prerequisites installed, you must create a DB named cloto in your MySQL server.
Ensure your mysql path is in your path. If not, you can add executing (change ``/usr/local/`` with your mysql folder):

.. code::

    $ export PATH=$PATH:/usr/local/mysql/bin

In addition, be sure you have installed mysql-devel package for development of MySQL applications.
You should be able to install it from yum or apt-get package managers.

Examples:

.. code::

    centos$ sudo yum install mysql-devel
    ubuntu$ sudo apt-get install mysql-devel

After all you must install fiware-cloto from pypi repository executing:

.. code::

    $ sudo pip install fiware-cloto

After finishing you must configure cloto configuration and ensure your database is created with mysql.

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Configuration file - Cloto
--------------------------
The configuration used by the fiware-cloto component is read from the configuration file.
This file is located here:

``/etc/fiware.d/fiware-cloto.cfg``

MYSQL cloto configuration must be filled before starting fiware-facts component, user and password are empty by default.
You can copy the `default configuration file <fiware_cloto/cloto_settings/fiware-cloto.cfg>`_ to the folder defined for your OS, and
complete data about cloto MYSQL configuration (user and password) and all openstack configuration.

In addition, user could have a copy of this file in other location and pass its location to the server in running
execution defining an environment variable called CLOTO_SETTINGS_FILE.

Options that user could define:

::

    [openstack]         # OPENSTACK information about KEYSTONE to validate tokens received
    OPENSTACK_URL: http://cloud.lab.fi-ware.org:4731/v2.0
    ADM_USER:
    ADM_PASS:
    ADM_TENANT_ID:
    ADM_TENANT_NAME:
    USER_DOMAIN_NAME: Default
    AUTH_API: v2.0

    [policy_manager]
    SETTINGS_TYPE: production
    DEFAULT_WINDOW_SIZE: 5
    MAX_WINDOW_SIZE: 10
    LOGGING_PATH: /var/log/fiware-cloto

    [context_broker]
    CONTEXT_BROKER_URL: http://130.206.81.44:1026/NGSI10
    NOTIFICATION_URL: http://127.0.0.1:5000/v1.0        # Public IP of fiware-facts module
    NOTIFICATION_TYPE: ONTIMEINTERVAL
    NOTIFICATION_TIME: PT5S

    [rabbitmq]
    RABBITMQ_URL: localhost     #URL Where RabbitMQ is listening (no port needed, it uses default port)

    [mysql]
    DB_CHARSET: utf8
    DB_HOST: localhost
    DB_NAME: cloto
    DB_USER:
    DB_PASSWD:

    [django]
    DEBUG: False
    DATABASE_ENGINE: django.db.backends.mysql
    ALLOWED_HOSTS: ['127.0.0.1', 'localhost']
    SECRET_KEY: TestingKey+faeogfjksrjgpjaspigjiopsjgvopjsopgvj         ### Must be a unique generated value. keep that key safe.

    [logging]
    level: INFO

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Running
=======

To run fiware-cloto, just execute:

.. code::

    $ gunicorn fiware_cloto.cloto.wsgi -b $IP

To stop fiware-cloto, you can stop gunicorn server, or kill it

NOTE: if you want to see gunicorn log if something is going wrong, you could execute the command before adding
``--log-file=-`` at the end of the command. This option will show the logs in your prompt.

Finally, ensure that you create a folder for logs ``/var/log/fiware-cloto/`` (by default), with the right permissions to write
in that folder.

::

    mkdir -m /var/log/fiware-cloto

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

API Overview
============

To create a new rule for a server, user should send the rule as body of a POST request to the cloto server, with the
condition and action that should be performed.

For example, this operation allows to create a specific rule associate to a server:

::

    curl -v -H 'X-Auth-Token: 86e096cd4de5490296fd647e21b7f0b4' -X POST http://130.206.81.71:8000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers/32c23ac4-230d-42b6-81f2-db9bd7e5b790/rules/ -d '{"action": {"actionName": "notify-scale", "operation": "scaleUp"}, "name": "ScaleUpRule", "condition": { "cpu": { "value": 98, "operand": "greater" }, "mem": { "value": 95, "operand": "greater equal"}}}'


The result of this operation is a JSON with the Id of the server affected and the ruleId of the created rule:

::

    {
        "serverId": "32c23ac4-230d-42b6-81f2-db9bd7e5b790",
        "ruleId": "68edb416-bfc6-11e3-a8b9-fa163e202949"
    }

Then user could perform a subscription to that rule with a new operation.

Please have a look at the `API Reference Documentation`_ section below and
at the `user and programmer guide <doc/user_guide.rst>`_ for more description of the possibilities and operations.

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

API Reference Documentation
---------------------------

- `FIWARE Policy Manager v1 (Apiary)`__

__ `FIWARE Policy Manager - Apiary`_

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Testing
=======

Unit tests
----------

Download source code from github

::

    $ git clone https://github.com/telefonicaid/fiware-cloto.git

To execute the unit tests, you must set the environment variable pointing to the settings_test file.
Then you can use coverage to execute the tests and obtain the percentage of lines coveved by the tests.
You must execute the tests from project folder ``fiware-cloto``.
Once you were inside the right location, execute the required commands:

::

    $ export DJANGO_SETTINGS_MODULE=fiware_cloto.cloto_settings.settings_tests
    $ export CLOTO_SETTINGS_FILE=$(pwd)/fiware_cloto/cloto_settings/fiware-cloto.cfg
    $ python fiware_cloto/manage.py test


`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

End-to-end tests
----------------

In order to check that fiware-cloto is up and running, you can execute a GET request similar to:

::

    curl -v -H 'X-Auth-Token: $AUTH_TOKEN' http://$HOST:8000/v1.0/$TENANT_ID/

Where:

- **$AUTH_TOKEN**: is a valid token owned by the user. You can request this token from keystone.
- **$HOST**: is the url/IP of the machine where fiware facts is installed, for example: (policymanager-host.org, 127.0.0.1, etc)
- **$TENANT_ID**: is a tenantId of the user, for example: 6571e3422ad84f7d828ce2f30373b3d4

the response should be similar to:

::

    {
        "owner": "Telefonica I+D",
        "doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fiware/index.php/Policy_Manager_Open_RESTful_API_Specification",
        "runningfrom": "15/08/14 10:12:45",
        "version": "1.7.0",
        "windowsize": 2
    }

Please refer to the `Installation and administration guide
<doc/admin_guide.rst#end-to-end-testing>`_ for details.

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Acceptance tests
----------------

Requirements

- Python 2.7 or newer
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)
- virtualenv installed (pip install virtalenv)
- Git installed (yum install git-core / apt-get install git)

Environment preparation:

- Create a virtual environment somewhere, e.g. in ENV (virtualenv ENV)
- Activate the virtual environment (source ENV/bin/activate)
- Change to the test/acceptance folder of the project
- Install the requirements for the acceptance tests in the virtual environment (pip install -r requirements.txt --allow-all-external).
- Configure file in fiware-cloto/tests/acceptance_tests/commons/configuration.py adding the keystone url, and a valid, user, password and tenant ID.

Tests execution

Change to the fiware-cloto/tests/acceptance_tests folder of the project if not already on it and execute:

::

       $ lettuce_tools

In the following document you will find the steps to execute automated
tests for the Policy Manager GE:

- `Policy Manager acceptance tests <fiware_cloto/cloto/tests/acceptance_tests/README.md>`_

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Advanced topics
===============

- `Installation and administration <doc/admin_guide.rst>`_
- `User and programmers guide <doc/user_guide.rst>`_
- `Open RESTful API Specification <doc/open_spec.rst>`_
- `Architecture Description <doc/architecture.rst>`_

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

Support
=======

Ask your thorough programming questions using stackoverflow and your general questions on FIWARE Q&A.
In both cases please use the tag fiware-bosun

`Top`__.

__ `FIWARE Policy Manager GE: Cloto`_

License
=======

\(c) 2013-2014 Telefónica I+D, Apache License 2.0


.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-cloto.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-cloto
.. |Coverage Status| image:: https://img.shields.io/coveralls/telefonicaid/fiware-cloto/develop.svg
   :target: https://coveralls.io/r/telefonicaid/fiware-cloto
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-cloto.svg
   :target: https://pypi.python.org/pypi/fiware-cloto/
.. |Pypi License| image:: https://img.shields.io/pypi/l/fiware-cloto.svg
   :target: https://pypi.python.org/pypi/fiware-cloto/


.. REFERENCES

.. _FIWARE: https://www.fiware.org/
.. _FIWARE Ops: https://www.fiware.org/fiware-operations/
.. _FIWARE Policy Manager - Apiary: https://jsapi.apiary.io/apis/policymanager/reference.html
.. _Fiware-cloto - GitHub issues: https://github.com/telefonicaid/fiware-cloto/issues/new
.. _FIWARE Policy Manager - Catalogue: http://catalogue.fiware.org/enablers/policy-manager-bosun
