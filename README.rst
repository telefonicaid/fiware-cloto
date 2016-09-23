.. _Top:

===============================
FIWARE Policy Manager GE: Cloto
===============================

|License Badge| |Documentation Badge| |StackOverflow| |Build Status| |Coverage Status| |Docker badge| |Pypi Version|

.. contents:: :local:

Introduction
============

This is the code repository for **FIWARE Policy Manager GE - Cloto**, a server
that provides a REST API to create rules associated to servers, subscribe
servers to Context Broker to get information about resources consumption of
those servers and launch actions described in rules when conditions are met.

This project is part of FIWARE_.
Check also the `FIWARE Catalogue entry for Policy Manager`__

__ `FIWARE Policy Manager - Catalogue`_

Any feedback on this documentation is highly welcome, including bugs, typos or
things you think should be included but aren't. You can use `github issues`__
to provide feedback.

__ `FIWARE Cloto - GitHub issues`_

Top_.


GEi overall description
=======================

Bosun GEri is the reference implementation of Policy Manager GE.

Bosun offers decision-making ability, independently of the type of resource
(physical/virtual resources, network, service, etc.) being able to solve
complex problems within the Cloud field by reasoning about the knowledge
base, represented by facts and rules. Bosun GEri provides the basic management
of cloud resources based on rules, as well as management of the corresponding
resources within FIWARE Cloud instances based on infrastructure physical
monitoring, resources and services security monitoring or whatever that
could be defined by facts, actions and rules.

The baseline for the Bosun GEri is PyCLIPS, which is a module to interact with
CLIPS expert system implemented in Python language. The reason to take PyCLIPS
is to extend the OpenStack ecosystem with an expert system, written in the same
language as the rest of the OpenStack services. Besides, It provides
notification service to your own HTTP server where you can define your
own actions based on the notifications launched by Policy Manager.
Last but not least, Bosun is integrated with the Monitoring GEri in order
to recover the information of the (virtual) system and calculate any possible
change on it based on the knowledge database defined for it.

Top_.


Components
----------

Fiware-Cloto
    Fiware-Cloto is part of FIWARE Policy Manager. It provides a REST API to
    create rules associated to servers, subscribe servers to Context Broker to
    get information about resources consumption of that servers and launch
    actions described in rules when conditions are met.

Fiware-Facts
    Server to process the incoming facts from `Orion Context Broker`_ and
    publish the result into a RabbitMQ queue to be analysed by Fiware-Cloto.
    The facts are the result of the server resources consumption.

For more information, please refer to the `documentation <doc/index.rst>`_.


Top_.


Build and Install
=================

Requirements
------------

Operating systems:

- CentOS (RedHat) and Ubuntu (Debian), being CentOS 7 the reference
  operating system.

Software dependencies:

- Python 2.7
- PyClips 1.0 (http://sourceforge.net/projects/pyclips/files/)
- RabbitMQ Server 3.3.0 or above (http://www.rabbitmq.com/download.html)
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)
- pip 7.0.0 or above (https://pip.pypa.io/en/stable/installing/)
- gcc-c++ and gcc libraries

This module also needs the installation of these other components:

- Fiware-facts module installed (https://github.com/telefonicaid/fiware-facts)
- A running instance of Orion Context Broker v0.28
  (https://github.com/telefonicaid/fiware-orion/releases/tag/0.28.0)
- Fiware-monitoring connected to the Orion instance to provide information
  about servers (https://github.com/telefonicaid/fiware-monitoring).

Top_.


Pre-Installation
----------------

You must create a database named ``cloto`` in your MySQL server before
installing this component.

In addition, be sure you have installed MySQL development libraries and tools
(using package managers such as yum or apt-get):

.. code::

    centos$ sudo yum install mysql-devel
    ubuntu$ sudo apt-get install mysql-client libmysqlclient-dev

Top_.


Configuration file
------------------

The configuration used by this component is read from the file located at
``/etc/fiware.d/fiware-cloto.cfg``, unless otherwise specified by environment
variable ``CLOTO_SETTINGS_FILE``.

MySQL settings of this configuration must be adjusted before starting the
fiware-facts component (for instance, user and password are empty by default):
please check section ``[mysql]``.

A sample configuration file may include the following (see default `here
<fiware_cloto/cloto_settings/fiware-cloto.cfg>`_):

::

    [openstack]
    # OPENSTACK information about KEYSTONE to validate tokens received
    OPENSTACK_URL: http://cloud.lab.fi-ware.org:4731/v2.0
    ADM_USER:
    ADM_PASS:
    ADM_TENANT_ID:
    ADM_TENANT_NAME:
    USER_DOMAIN_NAME: Default
    AUTH_API: v2.0

    [policy_manager]
    SECURITY_LEVEL: LOW
    SETTINGS_TYPE: production
    DEFAULT_WINDOW_SIZE: 5
    MAX_WINDOW_SIZE: 10
    LOGGING_PATH: /var/log/fiware-cloto

    [context_broker]
    CONTEXT_BROKER_URL: http://130.206.115.92:1026/v1
    # Public IP of fiware-facts module
    NOTIFICATION_URL: http://127.0.0.1:5000/v1.0
    NOTIFICATION_TYPE: ONTIMEINTERVAL
    NOTIFICATION_TIME: PT5S

    [rabbitmq]
    # URL Where RabbitMQ is listening (no port needed, it uses default port)
    RABBITMQ_URL: localhost

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
    ### Must be a unique generated value. keep that key safe.
    SECRET_KEY: TestingKey+faeogfjksrjgpjaspigjiopsjgvopjsopgvj

    [logging]
    level: INFO

Top_.


Installation
------------

Once pre-installation requirements are satisfied, please install fiware-cloto
package from PyPI repository:

.. code::

    $ sudo pip install fiware-cloto


Running
=======

To run fiware-cloto, just execute:

.. code::

    $ gunicorn fiware_cloto.cloto.wsgi -b BIND_ADDRESS

To stop fiware-cloto, you can stop gunicorn server, or kill it

NOTE: to enable writing gunicorn log messages to console, please add the option
``--log-file=-``; otherwise, if you prefer to write them into a file, just add
``--log-file=<log file name>``. By default, logs will be written in the folder
``/var/log/fiware-cloto/``: please ensure its permissions and owner are valid.


Running with supervisor
-----------------------

Optionally you can add a new layer to manage gunicorn process with a supervisor.
Just install supervisor on your system:

.. code::

    centos$ sudo yum install supervisor
    ubuntu$ sudo apt-get install supervisor

Copy the file `utils/cloto_start <utils/cloto_start>`_ to ``/etc/fiware.d`` and
ensure it has execution permissions:

.. code::

    $ sudo chmod a+x /etc/fiware.d/cloto_start

Then copy the file `utils/fiware-cloto.conf <utils/fiware-cloto.conf>`_ to
``/etc/supervisor/conf.d`` and start fiware-cloto using supervisor:

.. code::

    $ sudo supervisorctl reread
    $ sudo supervisorctl update
    $ sudo supervisorctl start fiware-cloto

To stop fiware-cloto just execute:

.. code::

    $ sudo supervisorctl stop fiware-cloto

NOTE: Supervisor provides an "event listener" to subscribe to the so-called
"event notifications". The purpose of the event notification/subscription
system is to provide a mechanism for arbitrary code to be run (e.g. send an
email, make an HTTP request, etc) when some condition is satisfied. That
condition usually has to do with subprocess state. For instance, you may
want to notify someone via email when a process crashes and is restarted
by Supervisor. For more information check also the `Supervisor Documentation`_.

Top_.


API Overview
============

To create a new rule for a server, user should send the rule as body of a POST
request to the Cloto server, with the condition and action that should be
performed.

For example, this operation allows to create a specific rule associate to a
server:

.. code::

    $ curl -v -H 'X-Auth-Token: 86e096cd4de5490296fd647e21b7f0b4' -X POST
    http://130.206.81.71:8000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers
    /32c23ac4-230d-42b6-81f2-db9bd7e5b790/rules/
    -d '{"action": {"actionName": "notify-scale", "operation": "scaleUp"},
    "name": "ScaleUpRule", "condition": { "cpu": { "value": 98, "operand": "greater" },
    "mem": { "value": 95, "operand": "greater equal"}}}'


The result of this operation is a JSON with the Id of the server affected and
the ruleId of the created rule:

::

    {
        "serverId": "32c23ac4-230d-42b6-81f2-db9bd7e5b790",
        "ruleId": "68edb416-bfc6-11e3-a8b9-fa163e202949"
    }

Then user could perform a subscription to that rule with a new operation.

Please have a look at the `API Reference Documentation`_ section below and
at the `user and programmer guide <doc/user_guide.rst>`_ for more description
of the possibilities and operations.

Note: Please keep in mind that the server (whose serverId in the previous example is
32c23ac4-230d-42b6-81f2-db9bd7e5b790 and tenantID is 6571e3422ad84f7d828ce2f30373b3d4)
has to be created in FIWARE Lab. Policy Manager does not take care about this instance
creation.

Top_.


API Reference Documentation
---------------------------

- `FIWARE Policy Manager v1 (Apiary)`__

__ `FIWARE Policy Manager - Apiary`_

Top_.


Testing
=======

Unit tests
----------

Download source code from github

.. code::

    $ git clone https://github.com/telefonicaid/fiware-cloto.git

To execute the unit tests, you must set the environment variable pointing to the
settings_test file. Then you can use coverage to execute the tests and obtain
the percentage of lines coveved by the tests. You must execute the tests from
project folder ``fiware-cloto``. Once you were inside the right location,
execute the required commands:

.. code::

    $ export DJANGO_SETTINGS_MODULE=fiware_cloto.cloto_settings.settings_tests
    $ export CLOTO_SETTINGS_FILE=$PWD/fiware_cloto/cloto_settings/fiware-cloto.cfg
    $ python fiware_cloto/manage.py test


Top_.


End-to-end tests
----------------

There are two ways to check that fiware-cloto is up and running:

The first one does not need authentication and you will get the server details:

.. code::

    $ curl -v -H 'X-Auth-Token: $AUTH_TOKEN' http://$HOST:8000/v1.0/$TENANT_ID/

Response should be similar to:

::

    {
        "owner": "Telefonica I+D",
        "doc": "http://docs.policymanager.apiary.io",
        "runningfrom": "16/02/03 16:16:27",
        "version": "2.3.0"
    }

The second one need authentication. You can execute a GET request similar to:

.. code::

    $ curl -v -H 'X-Auth-Token: $AUTH_TOKEN' http://$HOST:8000/v1.0/$TENANT_ID/

Where:

- **$AUTH_TOKEN**: is a valid token owned by the user. You can request this
  token from keystone.
- **$HOST**: is the url/IP of the machine where fiware facts is installed,
  for example: (policymanager-host.org, 127.0.0.1, etc)
- **$TENANT_ID**: is a tenantId of the user, for example:
  6571e3422ad84f7d828ce2f30373b3d4

The response should be similar to:

::

    {
        "owner": "Telefonica I+D",
        "doc": "http://docs.policymanager.apiary.io",
        "runningfrom": "16/02/03 16:16:27",
        "version": "2.3.0"
        "windowsize": 10
    }

Please refer to the `Installation and administration guide <doc/admin_guide.rst>`_
for details.

Top_.


Acceptance tests
----------------

Requirements

- Python 2.7
- pip 7.0.0 or above (https://pip.pypa.io/en/stable/installing/)
- virtualenv installed (pip install virtalenv)
- Git installed (yum install git-core / apt-get install git)

Environment preparation:

- Create a virtual environment somewhere, e.g. in ENV (virtualenv ENV)
- Activate the virtual environment (source ENV/bin/activate)
- Change to the test/acceptance folder of the project
- Install the requirements for the acceptance tests in the virtual environment
  (pip install -r requirements.txt --allow-all-external).
- Configure file in fiware_cloto/cloto/tests/acceptance/commons/configuration.py
  adding the keystone url, and a valid, user, password and tenant ID.

Tests execution

Change to the fiware_cloto/cloto/tests/acceptance folder of the project if not
already on it and execute:

.. code::

    $ behave

In the following document you will find the steps to execute automated
tests for the Policy Manager GE:

- `Policy Manager acceptance tests
  <fiware_cloto/cloto/tests/acceptance/README.rst>`_

Top_.


Advanced topics
===============

- `Installation and administration <doc/admin_guide.rst>`_
- `User and programmers guide <doc/user_guide.rst>`_
- `Open RESTful API Specification <doc/open_spec.rst>`_
- `Architecture Description <doc/architecture.rst>`_

Top_.


Support
=======

Ask your thorough programming questions using stackoverflow_ and your general
questions on `FIWARE Q&A`_. In both cases please use the tag *fiware-bosun*.

Top_.


License
=======

\(c) 2013-2016 Telefónica I+D, Apache License 2.0


.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-cloto.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-cloto
   :alt: Build Status
.. |Coverage Status| image:: https://img.shields.io/coveralls/telefonicaid/fiware-cloto/develop.svg
   :target: https://coveralls.io/r/telefonicaid/fiware-cloto
   :alt: Coverage Status
.. |Pypi Version| image:: https://badge.fury.io/py/fiware-cloto.svg
   :target: https://pypi.python.org/pypi/fiware-cloto/
   :alt: Version
.. |StackOverflow| image:: https://img.shields.io/badge/support-sof-yellowgreen.svg
   :target: https://stackoverflow.com/questions/tagged/fiware-bosun
   :alt: Help, ask questions
.. |License Badge| image:: https://img.shields.io/badge/license-Apache_2.0-blue.svg
   :target: LICENSE.txt
.. |Documentation Badge| image:: https://readthedocs.org/projects/fiware-cloto/badge/?version=latest
   :target: http://fiware-cloto.readthedocs.org/en/latest/?badge=latest
   :alt: License
.. |Docker badge| image:: https://img.shields.io/docker/pulls/fiware/bosun-cloto.svg
   :target: https://hub.docker.com/r/fiware/bosun-cloto
   :alt: Docker Pulls

.. REFERENCES

.. _FIWARE: https://www.fiware.org/
.. _FIWARE Q&A: https://ask.fiware.org
.. _FIWARE Ops: https://www.fiware.org/fiware-operations/
.. _FIWARE Cloto - GitHub issues: https://github.com/telefonicaid/fiware-cloto/issues/new
.. _FIWARE Policy Manager - Apiary: https://jsapi.apiary.io/apis/policymanager/reference.html
.. _FIWARE Policy Manager - Catalogue: http://catalogue.fiware.org/enablers/policy-manager-bosun
.. _Orion Context Broker: http://catalogue.fiware.org/enablers/publishsubscribe-context-broker-orion-context-broker
.. _stackoverflow: http://stackoverflow.com/questions/ask
.. _Supervisor Documentation: http://supervisord.org/events.html
