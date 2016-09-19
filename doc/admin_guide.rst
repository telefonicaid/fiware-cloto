Installation & Administration Guide
___________________________________


Policy Manager Installation
===========================

This guide tries to define the procedure to install the Policy Manager
in a machine, including its requirements and possible troubleshooting
that we could find during the installation. We have to talk about two
applications deployed in a Django server.

Please go to GitHub's `README <https://github.com/telefonicaid/fiware-cloto/blob/master/README.rst>`_ for more
documentation.


Requirements
------------

In order to execute the Policy Manager, it is needed to have previously
installed the following software of framework in the machine:

-  Rule engine dependencies:

   -  Python 2.7.6 `[1] <http://www.python.org/download/releases/2.7.6/>`_
   -  RabbitMQ 3.3.0 `[2] <http://www.rabbitmq.com/download.html>`_
   -  MySQL 5.6.14 or above `[3] <http://dev.mysql.com/downloads/mysql/>`_

-  Facts engine dependencies:

   -  Python 2.7.6 `[1] <http://www.python.org/download/releases/2.7.6/>`_
   -  Redis 2.8.8 `[4] <http://redis.io/download>`_

Rule engine installation
------------------------

There is no need to configure any special options in Django server. Run
as default mode.

Step 1: Install Python
~~~~~~~~~~~~~~~~~~~~~~

If you do not have Python installed by default, please, follow
instructions for your Operating System in the official page:
https://www.python.org/download/releases/2.7.6/

Step 2: Install RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~~~

To install RabbitMQ Server, it is better to refer official installation
page and follow instructions for the Operating System you use:
http://www.rabbitmq.com/download.html

After installation, you should start RabbitMQ. Note that you only need
one instance of RabbitMQ and It could be installed in a different server
than fiware-facts or Rule Engine.

Step 3: Install MySQL
~~~~~~~~~~~~~~~~~~~~~

To install MySQL Server, it is better to refer official installation
page and follow instructions for the Operating System you use:
http://dev.mysql.com/downloads/mysql/

You will need four packages:

::

    mysql-server
    mysql-client
    mysql-shared
    mysql-devel

After installation, you should create a user, create database called
'cloto' and give all privileges to the user for this database. The name of
that database could be different but should be configured in the config file
of fiware-facts and fiware-cloto.

To add a user to the server, please follow official documentation:
http://dev.mysql.com/doc/refman/5.5/en/adding-users.html


Step 4: Download and execute the Rule Engine server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Installing fiware-cloto

Install the component by executing the following instruction:

::

    sudo pip install fiware-cloto

It should show something like the following:

::

    Installing collected packages: fiware-cloto
        Running setup.py install for fiware-cloto
    Successfully installed fiware-cloto
    Cleaning up...


2. Configuring Rule engine

Before starting the rule engine, you should edit settings file and add it to the
default folder located in ``/etc/fiware.d/fiware-cloto.cfg``

In addition, user could have a copy of this file in other location and pass its
location to the server in running execution defining an environment variable
called CLOTO_SETTINGS_FILE.

You can find the reference file `here
<https://github.com/telefonicaid/fiware-cloto/blob/master/fiware_cloto/cloto_settings/fiware-cloto.cfg>`_.
You should copy this file into default folder and complete all empty keys.

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


You should also modify ``ALLOWED_HOSTS`` parameter adding
the hosts you want to be accesible from outside, your IP address, the
domain name, etc. An example could be like this:

::

    ALLOWED_HOSTS: ['127.0.0.1', 'localhost', 'policymanager.host.com','80.71.123.2’]


Finally, ensure that folder for logs (``/var/log/fiware-cloto/`` by default)
has the right permissions and owner.

In 2.5.0 release we added a new parameter called ``SECURITY_LEVEL``.
This parameter could have three values: ``[HIGH | MEDIUM | LOW]``
Depending of API version it will store user tokens in memory assuming that a
token will be valid for a time period. After this expiration time, token is
going to be verified with against keystone.

::

    Using v3:
     LOW: user token should be verified after 1h
     MEDIUM: User token should be verified after 30min
     HIGH: user token should be verified after each request

    Using v2.0:
     LOW: user tokens should be verified after 24h
     MEDIUM: user token should be verified after 6h
     HIGH: user token should be verified after each request

3. Starting the server

To run fiware-cloto, just execute:

.. code::

    $ gunicorn fiware_cloto.cloto.wsgi -b BIND_ADDRESS

Where BIND_ADDRESS is a valid network interface assigned with a public address.
If you execute the command with ``127.0.0.1`` fiware-cloto won't be accessible
from outside.

To stop fiware-cloto, you can stop gunicorn server, or kill it

NOTE: to enable writing gunicorn log messages to console, please add the option
``--log-file=-``; otherwise, if you prefer to write them into a file, just add
``--log-file=<log file name>``.


Facts installation
------------------

Step 1: Install python
~~~~~~~~~~~~~~~~~~~~~~

The process will be the same that be see in the previous section.


Step 2: Install Redis
~~~~~~~~~~~~~~~~~~~~~

Download, extract and compile Redis with:

::

    $ wget http://download.redis.io/releases/redis-2.8.8.tar.gz
    $ tar xzf redis-2.8.8.tar.gz
    $ cd redis-2.8.8
    $ make

The binaries that are now compiled are available in the src directory.
Run Redis with:

::

    $ src/redis-server

It execute the redis server on port 6379.

You can interact with Redis using the built-in client:

::

    $ src/redis-cli
    redis> set foo bar
    OK
    redis> get foo
    "bar"

Step 3: Install MySQL
~~~~~~~~~~~~~~~~~~~~~

The process is the same as process seen in the previous section. If fiware-facts
is being installed in the same system as fiware-cloto, you could omit this step.


Step 4: Download and execute the facts engine server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Installing fiware-facts

**Using pip**
Install the component by executing the following instruction:
::

    pip install fiware-facts

This operation will install the component in your python site-packages folder.

It should shown the following information when it is executed:

::

    Installing collected packages: fiware-facts
      Running setup.py install for fiware-facts

    Successfully installed fiware-facts
    Cleaning up...


2. Configuring fiware-facts

The configuration used by fiware-facts component is read from the configuration
file located at ``/etc/fiware.d/fiware-facts.cfg``

MySQL cloto configuration must be filled before starting fiware-facts component,
user and password are empty by default. You can copy the default configuration
file ``facts_conf/fiware_facts.cfg`` to the folder defined for your OS, and
complete data about cloto MySQL configuration (user and password).


In addition, user could have a copy of this file in other location and pass its
location to the server in running execution defining an environment variable
called FACTS_SETTINGS_FILE.

Options that user could define:
::

    [common]
     brokerPort: 5000       # Port listening fiware-facts
     clotoPort:  8000       # Port listening fiware-cloto
     redisPort:  6379       # Port listening redis-server
     redisHost:  localhost  # Address of redis-server
     rabbitMQ:   localhost  # Address of RabbitMQ server
     cloto:      127.0.0.1  # Address of fiware-cloto

    [mysql]
     host: localhost        # address of mysql that fiware-cloto is using
     user:                  # mysql user
     password:              # mysql password

    [logger_root]
     level: INFO            # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Finally, ensure that you create a folder for logs ``/var/log/fiware-facts/``
(by default), with the right permissions to write in that folder.

::

    mkdir -m /var/log/fiware-facts

3. Starting the server

Execute command:

::

    gunicorn facts.server:app -b $IP:5000

Where $IP should be the IP assigned to the network interface that should be
listening (ej. 192.168.1.33)

You can also execute the server with a different settings file providing an
environment variable with the location of the file:

::

    gunicorn facts.server:app -b $IP:5000
    --env FACTS_SETTINGS_FILE=/home/user/fiware-facts.cfg

NOTE: if you want to see gunicorn log if something is going wrong, you could
execute the command before adding ``--log-file=-`` at the end of the command.
This option will show the logs in your prompt (standard stderr). If you want
to store the log into a file just write ``--log-file=<log file name>``.


When you execute the server you can see some information about the server:

::

    2015-09-24 16:30:10,845 INFO policymanager.facts policymanager.facts 1.7.0

    2015-09-24 16:30:10,846 INFO policymanager.facts Running in stand alone mode
    2015-09-24 16:30:10,846 INFO policymanager.facts Port: 5000
    2015-09-24 16:30:10,846 INFO policymanager.facts PID: 19472

    2015-09-24 16:30:10,846 INFO policymanager.facts
                                              https://github.com/telefonicaid/fiware-facts



    2015-09-24 16:30:10,896 INFO policymanager.facts Waiting for windowsizes

Sanity check procedures
=======================

The Sanity Check Procedures are the steps that a System Administrator
will take to verify that an installation is ready to be tested. This is
therefore a preliminary set of tests to ensure that obvious or basic
malfunctioning is fixed before proceeding to unit tests, integration
tests and user validation.

End to End testing
------------------

Although one End to End testing must be associated to the Integration
Test, we can show here a quick testing to check that everything is up
and running. For this purpose we send a request to our API in order to
test the credentials that we have from then and obtain a valid token to
work with.

In order to make a probe of the different functionalities related to the
Policy Manager, we start with the obtention of a valid token for a
registered user. Due to all operations of the Policy Manager are using
the security mechanism which is used in the rest of the cloud component,
it is needed to provide a security token in order to continue with the
rest of operations. For this operation we need to execute the following
curl sentence.

::

    curl -d '{"auth": {"tenantName": $TENANT,
    "passwordCredentials":{"username": $USERNAME, "password": $PASSWORD}}}'
    -H "Content-type: application/json" -H "Accept: application/xml"
    http://130.206.80.100:35357/v2.0/tokens

Both $TENANT (Project), $USERNAME and $PASSWORD must be values
previously created in the OpenStack Keystone. The IP address
10.95.171.115 and the Port 35357 are the data of our internal
installation of IdM, if you planned to execute it you must changed it by
the corresponding IP and Port of the FIWARE Keystone or IdM IP and Port
addresses.

We obtained two data from the previous sentence:

-  X-Auth-Token

::

    <token expires="2012-10-25T16:35:42Z" id="a9a861db6276414094bc1567f664084d">

-  Tenant-Id

::

    <tenant enabled="true" id="c907498615b7456a9513500fe24101e0" name=$TENANT>

After it, we can check if the Policy Manager is up and running with a
single instruction which is used to return the information of the status
of the processes together with the queue size.

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d'
    -X GET http://130.206.81.71:8000/v1.0/c907498615b7456a9513500fe24101e0

This operation will return the information regarding the tenant details
of the execution of the Policy Manager

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 08:25:17 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8
    {
        "owner": "Telefonica I+D", 
        "doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php/
                                     FIWARE.OpenSpecification.Details.Cloud.PolicyManager",
        "runningfrom": "14/04/09 07:45:22", 
        "version": 1.0, 
        "windowsize": 5
    }

For more details to use this GE, please refer to the User & Programmers Guide.

List of Running Processes
-------------------------

Due to the Policy Manager basically is running over the python process,
the list of processes must be only the python and redis in case of the
facts engine. If we execute the following command:

::

    ps -ewf | grep 'redis\|Python' | grep -v grep

It should show something similar to the following:

::

    UID   PID  PPID   C   STIME     TTY       TIME   CMD
    501  5287   343   0  9:42PM ttys001    0:02.49   ./redis-server *:6379
    501  5604   353   0  9:40AM ttys002    0:00.20 /Library/Frameworks/Python.framework/
    Versions/2.7/Resources/Python.app/Contents/MacOS/Python facts.py

Where you can see the Redis server, and the run process to launch the
Python program.

In case of the rule engine node, if we execute the following command:

::

    ps -ewf | grep 'rabbitmq-server\|python' | grep -v grep

It should show something similar to the following:

::

    UID        PID  PPID  C    SZ   RSS PSR STIME TTY          TIME CMD
    root      1584     1  0 15:31 ?        00:00:00 /bin/sh /etc/rc3.d/
    S80rabbitmq-server start
    root      1587  1584  0 15:31 ?        00:00:00 /bin/bash -c ulimit -S -c 0
    >/dev/null 2>&1 ; /usr/sbin/rabbitmq-server
    root      1589  1587  0 15:31 ?        00:00:00 /bin/sh /usr/sbin/rabbitmq-server
    root      1603  1589  0 15:31 ?        00:00:00 su rabbitmq -s /bin/sh -c
    /usr/lib/rabbitmq/bin/rabbitmq-server
    root      2038  2011  0 15:32 ?        00:00:01 python cloto/environmentManager.py
    root      2039  2011  1 15:32 ?        00:00:38 /usr/bin/python manage.py
    runserver 172.30.1.119:8000

where we can see the rabbitmq process, the run process to launch the
Python program and the clips program.

Network interfaces Up & Open
----------------------------

Taking into account the results of the ps commands in the previous
section, we take the PID in order to know the information about the
network interfaces up & open. To check the ports in use and listening,
execute the command:

::

    lsof -i | grep "$PID1\|$PID2" 

Where $PID1 and $PID2 are the PIDs of Python and Redis server obtained
at the ps command described before, in the previous case 5287
(redis-server) and 5604 (Python). The expected results must be something
similar to the following:

::

    COMMAND    PID USER    FD  TYPE             DEVICE SIZE/OFF NODE NAME
    redis-ser 5287  fla    4u  IPv6 0x8a557b63682bb0ef      0t0  TCP *:6379 (LISTEN)
    redis-ser 5287  fla    5u  IPv4 0x8a557b636a696637      0t0  TCP *:6379 (LISTEN)
    redis-ser 5287  fla    6u  IPv6 0x8a557b63682b9fef      0t0  TCP localhost:6379->
    localhost:56046 (ESTABLISHED)
    Python    5604  fla    7u  IPv6 0x8a557b63682bacaf      0t0  TCP localhost:56046->
    localhost:6379 (ESTABLISHED)
    Python    5604  fla    9u  IPv4 0x8a557b6369c90637      0t0  TCP *:commplex-main
    (LISTEN)

In case of rule engine, the result will we the following:

::

    COMMAND    PID USER    FD  TYPE             DEVICE SIZE/OFF NODE NAME
    python    2039       root    3u  IPv4  13290      0t0  UDP *:12027 
    python    2039       root    4u  IPv4  13347      0t0  TCP policymanager.novalocal
    :irdmi (LISTEN)
    python    2044       root    3u  IPv6  13354      0t0  TCP localhost:38391->localhost
    :amqp (ESTABLISHED)

Databases
---------

The last step in the sanity check, once that we have identified the
processes and ports is to check the database that have to be up and
accept queries. For the first one, if we execute the following commands
inside the code of the rule engine server:

::

    $ mysql -u user -p

Where user is the administration user defined for cloto database. The previous
command should ask you for the password and after that show you:

::

    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 155286
    Server version: 5.6.14 MySQL Community Server (GPL)

    Copyright (c) 2000, 2013, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    mysql>

In order to show the different tables contained in this database, we
should execute the following commands with the result that we show here:

::

    mysql> SHOW TABLES FROM cloto;
    +----------------------------+
    | Tables_in_cloto            |
    +----------------------------+
    | auth_group                 |
    | auth_group_permissions     |
    | auth_permission            |
    | auth_user                  |
    | auth_user_groups           |
    | auth_user_user_permissions |
    | cloto_entity               |
    | cloto_entity_specificrules |
    | cloto_entity_subscription  |
    | cloto_rule                 |
    | cloto_serverinfo           |
    | cloto_specificrule         |
    | cloto_subscription         |
    | cloto_tenantinfo           |
    | django_content_type        |
    | django_session             |
    | django_site                |
    +----------------------------+

Now, we can execute a simple test query in order to check the content of
the table:

::

    mysql> select * from cloto.cloto_serverinfo;

It should return with the following information:

::

    +----+----------------+---------+---------------------+--------+
    | id | owner          | version | runningfrom         | doc    |
    +----+----------------+---------+---------------------+--------+
    |  1 | Telefonica I+D |       1 | 2014-10-02 14:04:41 | {file} |
    +----+----------------+---------+---------------------+--------+

Where {file} is the path to the OpenSpecification file whose value is
https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php/FIWARE.OpenSpecification.Details.Cloud.PolicyManager

Diagnosis Procedures
====================

The Diagnosis Procedures are the first steps that a System Administrator
will take to locate the source of an error in a GE. Once the nature of
the error is identified with these tests, the system admin will very
often have to resort to more concrete and specific testing to pinpoint
the exact point of error and a possible solution. Such specific testing
is out of the scope of this section.

Resource availability
---------------------

The resource availability in the node should be at least 2Gb of RAM and
8GB of Hard disk in order to prevent enabler’s bad performance in both
nodes. This means that bellow these thresholds the enabler is likely to
experience problems or bad performance.

Remote Service Access
---------------------

We have internally two components to connect, the Rule engine component
and the facts engine component. After that two internals component, we
should connect with the the IdM GE. An administrator to verify that such
links are available will use this information.

The first step is to check that the facts engine is up and running, for
this purpose we can execute the following curl command, which is a
simple GET operation:

::

    root@fiware:~# curl http://$IP:$PORT/v1.0

The variable will be the IP direction in which we have installed the
facts engine. This request should return the status of the server if it
is working properly:

::

    {"fiware-facts":"Up and running..."}

In order to check the connectivity between the rule engine and the IdM
GE, due to it must obtain a valid token and tenant for a user and
organization with the following curl commands:

::

    root@fiware:~# curl
    -d '{"auth": {"tenantName": "<MY_ORG_NAME>",
    "passwordCredentials":{"username": "<MY_USERNAME>", "password": "<MY_PASS>"}}}'
    -H "Content-type: application/json" -H "Accept: application/xml"
    http://<KEYSTONE_HOST>:<KEYSTONE_PORT>/v2.0/tokens

The will be the name of my Organization/Tenant/Project predefined in the
IdM GE (aka Keystone). The and variables will be the user name and
password predefined in the IdM GE and finally the and variables will be
the IP direction and port in which we can find the IdM GE (aka
Keystone). This request should return one valid token for the user
credentials together with more information in a xml format:

::

    <?xml version="1.0" encoding="UTF-8"?>
    <access xmlns="http://docs.openstack.org/identity/api/v2.0">
      <token expires="2012-06-30T15:12:16Z" id="9624f3e042a64b4f980a83afbbb95cd2">
        <tenant enabled="true" id="30c60771b6d144d2861b21e442f0bef9" name="FIWARE">
          <description>FIWARE Cloud Chapter demo project</description>
        </tenant>
      </token>
      <serviceCatalog>
      …
      </serviceCatalog>
      <user username="fla" id="b988ec50efec4aa4a8ac5089adddbaf9" name="fla">
        <role id="32b6e1e715f14f1dafde24b26cfca310" name="Member"/>
      </user>
    </access>

With this information (extracting the token id), we can perform a GET
operation to the rule engine in order to get the information related to
the window size associated to a tenant. For this purpose we can execute
the following curl commands:

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d'
    -X GET "http://<Rule Engine HOST>:8000/v1.0/c8da25c7a373473f8e8945f5b0da8217"

The variable will be the IP direction in which we have installed the
Rule engine API functionality. This request should return the valid info
for this tenant in the following json response structure:

::

    {
        "owner": "Telefonica I+D", 
        "doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php
                                    /FIWARE.OpenSpecification.Details.Cloud.PolicyManager",
        "runningfrom": "14/04/11 12:32:29", 
        "version": "1.0",
        "windowsize": 5
    }

Resource consumption
--------------------

State the amount of resources that are abnormally high or low. This
applies to RAM, CPU and I/O. For this purpose we have differentiated
between:

-  Low usage, in which we check the resources that the JBoss or Tomcat
   requires in order to load the IaaS SM.
-  High usage, in which we send 100 concurrent accesses to the Claudia
   and OpenStack API.

The results were obtained with a top command execution over the following machine configuration:

.. list-table:: Machine Info
   :header-rows: 1
   :widths: 10 10 10
   :stub-columns: 1

   *  -  Machine
      -  Rule Engine Node
      -  Facts Engine Node
   *  -  Type Machine
      -  Virtual Machine
      -  Virtual Machine
   *  -  CPU
      -  1 core @ 2,4Ghz
      -  Intel(R) Xeon(R) CPU X5650 Dual Core @ 2.67GHz
   *  -  RAM
      -  2GB
      -  2GB
   *  -  HDD
      -  20GB
      -  20GB
   *  -  Operating System
      -  CentOS 6.3
      -  CentOS 6.3

The results of requirements both RAM, CPU and I/O to HDD in case of
Rule engine node is shown in the following table:

.. list-table:: Resource Consumption (in JBoss node)
   :header-rows: 1
   :widths: 10 10 10
   :stub-columns: 1

   *  -  Characteristic
      -  Low Usage
      -  High Usage
   *  -  RAM
      -  1,2GB ~ 70%
      -  1,4GB ~ 83,5%
   *  -  CPU
      -  1,3% of a 2400MHz
      -  95% of a 2400MHZ
   *  -  I/O HDD
      -  6GB
      -  6GB

And the results of requirements both RAM, CPU and I/O to HDD in case
of Tomcat node is shown in the following table:

.. list-table:: Resource Consumption (in Tomcat node)
   :header-rows: 1
   :widths: 10 10 10
   :stub-columns: 1

   *  -  Characteristic
      -  Low Usage
      -  High Usage
   *  -  RAM
      -  1,2GB ~ 63%
      -  1,5GB ~ 78%
   *  -  CPU
      -  0,8% of a 2400MHz
      -  90% of a 2400MHZ
   *  -  I/O HDD
      -  6GB
      -  6GB

I/O flows
---------

The rule engine application is hearing from port 8000 and the Fact-Gen
application (by default) is hearing in the port 5000. Please refer to
the installation process in order to know exactly which was the port
selected.
