FIWARE Policy Manager - Installation and Administration Guide
_____________________________________________________________

Policy Manager Installation
===========================

This guide tries to define the procedure to install the Policy Manager
in a machine, including its requirements and possible troubleshooting
that we could find during the installation. We have to talk about two
applications deployed in a Django server.

Final deployment into a production system should be performed in apache
server with mod wsgi.

You could find instructions for deploy policy Manager in apache +
mod\_wgsi at the end of this document.

Requirements
------------

In order to execute the Policy Manager, it is needed to have previously
installed the following software of framework in the machine:

-  Rule engine dependencies:

   -  Python 2.7.6
      `1 <http://www.python.org/download/releases/2.7.6/>`__.
   -  PyClips 1.0 `2 <http://sourceforge.net/projects/pyclips/files/>`__
   -  RabbitMQ 3.3.0 `3 <http://www.rabbitmq.com/download.html>`__
   -  MySQL 5.6.14 or above
      `4 <http://dev.mysql.com/downloads/mysql/>`__

-  Facts engine dependencies:

   -  Python 2.7.6
      `5 <http://www.python.org/download/releases/2.7.6/>`__.
   -  Redis 2.8.8 `6 <http://redis.io/download>`__

Rule engine installation
------------------------

There is no need to configure any special options in django server. Run
as default mode.

Step 1: Install python
~~~~~~~~~~~~~~~~~~~~~~

If you do not have python installed by default, please, follow
instructions for your Operating System in the official page:
https://www.python.org/download/releases/2.7.6/

Step 2: Install pyclips
~~~~~~~~~~~~~~~~~~~~~~~

Download pyclips from
http://sourceforge.net/projects/pyclips/files/pyclips/pyclips-1.0

To install pyClips execute this following commands:

| ``   $ tar -xvf pyclips-1.0.X.Y.tar.gz``
| ``   $ cd pyclips``
| ``   $ python setup.py build``
| ``   $ su -c "python setup.py install"``

Maybe you need to execute these commands using sudo.

If everything was OK, you should not receive any error.

Step 3: Install RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~~~

To install RabbitMQ Server, it is better to refer official installation
page and follow instructions for the Operating System you use:
http://www.rabbitmq.com/download.html

After installation, you should start RabbitMQ. Note that you only need
one instance of RabbitMQ and It could be installed in a different server
than fiware-facts or Rule Engine.

Step 4: Install MySQL
~~~~~~~~~~~~~~~~~~~~~

To install MySQL Server, it is better to refer official installation
page and follow instructions for the Operating System you use:
http://dev.mysql.com/downloads/mysql/

You will need four packages:

| ``mysql-server``
| ``mysql-client``
| ``mysql-shared``
| ``mysql-devel``

After installation, you should create a user, create database called
'cloto' and give all privileges to the user for this database.

To add a user to the server, please follow official documentation:
http://dev.mysql.com/doc/refman/5.5/en/adding-users.html

Step 5: Download and execute the Rule Engine server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the component by executing the following instruction:

::

    git clone git@github.com:telefonicaid/fiware-cloto.git

It should show something like the following:

::

    Cloning into 'fiware-cloto'...
    remote: Counting objects: 1483, done.
    remote: Compressing objects: 100% (692/692), done.
    remote: Total 1483 (delta 951), reused 1261 (delta 743)
    Receiving objects: 100% (1483/1483), 196.42 KiB | 0 bytes/s, done.
    Resolving deltas: 100% (951/951), done.
    Checking connectivity... done.

Go to the directory where we download the server and follow next steps:

1. Installing fiware-cloto

::

    $ sh install.sh

This script will install fiware-cloto in /opt/policyManager and it will
ask you for some configuration parameters. Please, ensure you have all
this data before starting the script in order to install fiware-cloto
easiest.

| ``   - Keystone URL.``
| ``   - Keystone admin user, password and tenant.``
| ``   - Mysql user and password.``

If you do not provide previous data to installer, you must complete all
configuration fields described in step, write mysql user and password in
db.cfg file located in cloto folder and relaunch installation script
saying NO again when it asks you about configuration data.

At the end of the script it should shown a message without errors
similar to:

::

    Cleaning up...
    Creating tables ...
    Installing custom SQL ...
    Installing indexes ...
    Installed 0 object(s) from 0 fixture(s)
    ...
    ...Done
    Please check file located in /opt/policyManager/fiware-cloto to configure all parameters 
    and check all configuration described in README.md before starting fiware-cloto
    ### To execute fiware-cloto you must execute 'service fiware-cloto start' ###

2. Configuring Rule engine

Before starting the rule engine, you should edit configuration.py
located at cloto folder. Constants you need to complete are:

| ``- All in # OPENSTACK CONFIGURATION: Openstack information (If you provide this information in the install script you do not need to edit)``
| ``- RABBITMQ_URL: URL Where RabbitMQ is listening (no port needed, it uses default port) ``
| ``- CONTEXT_BROKER_URL: URL where Context Broker is listening``
| ``- NOTIFICATION_URL: URL where notification service is listening (This service must be implemented by the user)``

in addition you could modify other constants like NOTIFICATION\_TIME, or
DEFAULT\_WINDOW\_SIZE.

Finally you should modify ALLOWED\_HOSTS parameter in settings.py adding
the hosts you want to be accesible from outside, your IP address, the
domain name, etc. An example could be like this:

``ALLOWED_HOSTS = ['policymanager.host.com','80.71.123.2’]``

3. Starting the server

At end of installation you could see ### To execute fiware-cloto you
must execute 'service fiware-cloto start' ###, well this way is for
starting server in a production system, please, check instructions in
the section "Installation into a Production System" to execute policy
manager using that way.

If you prefer play with policy manager locally, you could start the
server using this following command:

::

    $ python manage.py runserver 8000

It should shown the following information when it is executed:

::

    Validating models...

    0 errors found
    April 11, 2014 - 14:12:42
    Django version 1.5.5, using settings 'cloto.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

If you want to start Rule Engine using other IP address, you should
execute:

::

    $ python manage.py runserver <IP>:8000

Where IP is a valid network interface assigned. It is recommended if
your Rule Engine will be called from different networks.

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

Step 3: Download and execute the facts engine server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the component by executing the following instruction:

::

    git clone git@github.com:telefonicaid/fiware-facts.git

It should show something like the following:

::

    Cloning into 'fiware-facts'...
    remote: Counting objects: 211, done.
    remote: Compressing objects: 100% (136/136), done.
    remote: Total 211 (delta 118), reused 152 (delta 63)
    Receiving objects: 100% (211/211), 65.79 KiB | 0 bytes/s, done.
    Resolving deltas: 100% (118/118), done.
    Checking connectivity... done.

Go to the directory where we download the server and execute the
following commands:

Go to the directory where we download the server and execute the
following commands:

1. Installing all dependencies

::

    $ sudo pip install -r requirements.txt

It should install all dependencies showing at the end a message similar
to:

::

    Successfully installed redis flask gevent pika
    Cleaning up...

Then, after the installation of the requirements associated to the facts
engine, it is hour to execute the server, just run:

::

    $ python facts.py

It should shown the following information when it is executed:

::

    2014-04-11 10:42:19,344 INFO policymanager.facts policymanager.facts 1.0.0

    2014-04-11 10:42:19,344 INFO policymanager.facts Running in stand alone mode
    2014-04-11 10:42:19,345 INFO policymanager.facts Port: 5000
    2014-04-11 10:42:19,345 INFO policymanager.facts PID: 6059

    2014-04-11 10:42:19,345 INFO policymanager.facts https://github.hi.inet/telefonicaid/fiware-facts

Installation into a Production System
=====================================

If you want to deploy Policy Manager with this propose, you should
deploy on Apache Server with mod\_wsgi

Rule Engine
-----------

Step 1: Install Apache with mod\_wsgi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apache used to be installed on most of linux systems. If you do not have
apache installed, try downloading from your package manager like apt-get
or yum Also you can download from the official site
http://httpd.apache.org/

After install apache, The official mod\_wsgi documentation it’s the best
guide for all the details about how to use mod\_wsgi on your system.
https://code.google.com/p/modwsgi/wiki/InstallationInstructions

Step 2: Apache configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you’ve got mod\_wsgi installed and activated, edit your httpd.conf
file and add:

 WSGIScriptAlias / PATH_TO_fiware-cloto/cloto/wsgi.py
 WSGIPythonPath PATH_TO_fiware-cloto

 <Directory PATH_TO_fiware-cloto/cloto>
 <Files wsgi.py>
 Order deny,allow
 Allow from all
 </Files>
 </Directory>

 <Directory /var/log/fiware-cloto>
 <Files RuleEngine.log>
 Allow from all
 </Files>
 </Directory>

If you have apache above 2.2 version, you have to replace "Allow form
all" with "Require all granted"

In addition you must add the port listening 8000 in case of fiware-cloto

``Listen 8000``

Step 3: Run Server
~~~~~~~~~~~~~~~~~~

Finally , run apache service to have a fiware-cloto instance running

``service fiware-cloto start``

Facts
-----

Step 1: Install Apache with mod\_wsgi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is the same as described in step 1 of Rule Engine. please
follow those instructions.

Step 2: Apache configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you’ve got mod\_wsgi installed and activated, edit your httpd.conf
file and add:

 WSGIScriptAlias / PATH_TO_fiware-facts/facts.py
 WSGIPythonPath PATH_TO_fiware-facts

 <Directory PATH_TO_fiware-facts>
 <Files facts.py>
 Order deny,allow
 Allow from all
 </Files>
 </Directory>

 <Directory /var/log/fiware-facts>
 <Files fiware-facts.log>
 Allow from all
 </Files>
 </Directory>

If you have apache above 2.2 version, you have to replace "Allow form
all" with "Require all granted"

In addition you must add the port listening 5000 in case of fiware-facts

``Listen 5000``

Step 3: Run apache
~~~~~~~~~~~~~~~~~~

Finally , run apache service to have a fiware-facts instance running

``sudo apachectl start``

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

    curl -d '{"auth": {"tenantName": $TENNANT, "passwordCredentials":{"username": $USERNAME, "password": $PASSWORD}}}' 
    -H "Content-type: application/json" -H "Accept: application/xml"  http://130.206.80.100:35357/v2.0/tokens

Both $TENNANT (Project), $USERNAME and $PASSWORD must be values
previously created in the OpenStack Keystone. The IP address
10.95.171.115 and the Port 35357 are the data of our internal
installation of IdM, if you planned to execute it you must changed it by
the corresponding IP and Port of the FIWARE Keystone or IdM IP and Port
addresses.

We obtained two data from the previous sentence:

-  X-Auth-Token

::

    <token expires="2012-10-25T16:35:42Z" id="a9a861db6276414094bc1567f664084d">

-  Tennant-Id

::

    <tenant enabled="true" id="c907498615b7456a9513500fe24101e0" name=$TENNANT>

After it, we can check if the Policy Manager is up and running with a
single instruction which is used to return the information of the status
of the processes together with the queue size.

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d' -X GET http://130.206.81.71:8000/v1.0/c907498615b7456a9513500fe24101e0

This operation will return the information regarding the tenant details
of the execution of the Policy Manager

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 08:25:17 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8
    {
        "owner": "Telefonica I+D", 
        "doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php/FIWARE.OpenSpecification.Details.Cloud.PolicyManager", 
        "runningfrom": "14/04/09 07:45:22", 
        "version": 1.0, 
        "windowsize": 5
    }

For more details to use this GE, please refer to the `Policy Manager -
User and Programmers
Guide <Policy_Manager_-_User_and_Programmers_Guide>`__.

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
    501  5604   353   0  9:40AM ttys002    0:00.20 /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python facts.py

Where you can see the Redis server, and the run process to launch the
Python program.

In case of the rule engine node, if we execute the following command:

::

    ps -ewf | grep 'rabbitmq-server\|python' | grep -v grep

It should show something similar to the following:

::

    UID        PID  PPID  C    SZ   RSS PSR STIME TTY          TIME CMD
    root      1584     1  0 15:31 ?        00:00:00 /bin/sh /etc/rc3.d/S80rabbitmq-server start
    root      1587  1584  0 15:31 ?        00:00:00 /bin/bash -c ulimit -S -c 0 >/dev/null 2>&1 ; /usr/sbin/rabbitmq-server
    root      1589  1587  0 15:31 ?        00:00:00 /bin/sh /usr/sbin/rabbitmq-server
    root      1603  1589  0 15:31 ?        00:00:00 su rabbitmq -s /bin/sh -c /usr/lib/rabbitmq/bin/rabbitmq-server 
    root      2038  2011  0 15:32 ?        00:00:01 python cloto/environmentManager.py
    root      2039  2011  1 15:32 ?        00:00:38 /usr/bin/python manage.py runserver 172.30.1.119:8000

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
    redis-ser 5287  fla    6u  IPv6 0x8a557b63682b9fef      0t0  TCP localhost:6379->localhost:56046 (ESTABLISHED)
    Python    5604  fla    7u  IPv6 0x8a557b63682bacaf      0t0  TCP localhost:56046->localhost:6379 (ESTABLISHED)
    Python    5604  fla    9u  IPv4 0x8a557b6369c90637      0t0  TCP *:commplex-main (LISTEN)

In case of rule engine, the result will we the following:

::

    COMMAND    PID USER    FD  TYPE             DEVICE SIZE/OFF NODE NAME
    python    2039       root    3u  IPv4  13290      0t0  UDP *:12027 
    python    2039       root    4u  IPv4  13347      0t0  TCP policymanager.novalocal:irdmi (LISTEN)
    python    2044       root    3u  IPv6  13354      0t0  TCP localhost:38391->localhost:amqp (ESTABLISHED)

Databases
---------

The last step in the sanity check, once that we have identified the
processes and ports is to check the database that have to be up and
accept queries. For the first one, if we execute the following commands
inside the code of the rule engine server:

::

    $ sqlite3 cloto.db

Where cloto.db is the file that contains the information of the SQLite
Databases. The previous command should show something like the
following:

::

    SQLite version 3.6.20
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> 

In order to show the different tables contained in this database, we
should execute the following commands with the result that we show here:

::

    sqlite> .tables
    auth_group                  cloto_rule                
    auth_group_permissions      cloto_serverinfo          
    auth_permission             cloto_specificrule        
    auth_user                   cloto_subscription        
    auth_user_groups            cloto_tenantinfo          
    auth_user_user_permissions  django_content_type       
    cloto_entity                django_session            
    cloto_entity_specificrules  django_site               
    cloto_entity_subscription 
    sqlite> 

Now, we can execute a simple test query in order to check the content of
the table:

::

    sqlite> .header on
    sqlite> .width 2 14 7 26 80
    sqlite> .mode column
    sqlite> select * from cloto_serverinfo;

It is important that you execute the command "*.header on*\ ", which
allows you showing the header info of the tables. The other instructions
are used in order to show the information in a more friendly way. And it
should return with the following information:

::

    id  owner           version  runningfrom                 doc                                                                             
    --  --------------  -------  --------------------------  --------------------------------------------------------------------------------
    1   Telefonica I+D  1.0      2014-04-11 12:32:29.604238  https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php/FIWAR

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

    root@fiware:~# curl -d '{"auth": {"tenantName": "<MY_ORG_NAME>", "passwordCredentials":{"username": "<MY_USERNAME>", "password": "<MY_PASS>"}}}' -H "Content-type: application/json" -H "Accept: application/xml"  http://<KEYSTONE_HOST>:<KEYSTONE_PORT>/v2.0/tokens

The will be the name of my Organization/Tennat/Project predefined in the
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

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d' -X GET "http://<Rule Engine HOST>:8000/v1.0/c8da25c7a373473f8e8945f5b0da8217"

The variable will be the IP direction in which we have installed the
Rule engine API functionality. This request should return the valid info
for this tenant in the following json response structure:

::

    {
        "owner": "Telefonica I+D", 
        "doc": "https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/index.php/FIWARE.OpenSpecification.Details.Cloud.PolicyManager", 
        "runningfrom": "14/04/11 12:32:29", 
        "version": 1.0, 
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

| 
|  The results were obtained with a top command execution over the
following machine configuration:

| 
| {\| style="background:#cccc99;color:black;width:50%;" border="1"
cellpadding="3" cellspacing="0" align="center" \|+ Machine Info ! !!
Rule Engine Node !! Facts Engine Node \|- style="background:white;
color:black" align="center" ! Type Machine \| Virtual Machine \| Virtual
Machine \|- style="background:#f0f0f0; color:black" align="center" ! CPU
\| 1 core @ 2,4Ghz \| Intel(R) Xeon(R) CPU X5650 Dual Core @ 2.67GHz \|-
style="background:white; color:black" align="center" ! RAM \| 2GB \| 2GB
\|- style="background:white; color:black" align="center" ! HDD \| 20GB
\| 20GB \|- style="background:white; color:black" align="center" !
Operating System \| CentOS 6.3 \| CentOS 6.3 \|}

| 
|  The results of requirements both RAM, CPU and I/O to HDD in case of
Rule engine node is shown in the following table:

| 
| {\| style="background:#cccc99;color:black;width:50%;" border="1"
cellpadding="3" cellspacing="0" align="center" \|+ Resource Consumption
(in JBoss node) ! !! Low Usage !! High Usage \|-
style="background:white; color:black" align="center" ! RAM \| 1,2GB ~
70% \| 1,4GB ~ 83,5% \|- style="background:#f0f0f0; color:black"
align="center" ! CPU \| 1,3% of a 2400MHz \| 95% of a 2400MHZ \|-
style="background:white; color:black" align="center" ! I/O HDD \| 6GB \|
6GB \|}

| 
| And the results of requirements both RAM, CPU and I/O to HDD in case
of Tomcat node is shown in the following table:

| 
| {\| style="background:#cccc99;color:black;width:50%;" border="1"
cellpadding="3" cellspacing="0" align="center" \|+ Resource Consumption
(in Tomcat node) ! !! Low Usage !! High Usage \|-
style="background:white; color:black" align="center" ! RAM \| 1,2GB ~
63% \| 1,5GB ~ 78% \|- style="background:#f0f0f0; color:black"
align="center" ! CPU \| 0,8% of a 2400MHz \| 90% of a 2400MHZ \|-
style="background:white; color:black" align="center" ! I/O HDD \| 6GB \|
6GB \|}

I/O flows
---------

The rule engine application is hearing from port 8000 and the Fact-Gen
application (by default) is hearing in the port 5000. Please refer to
the installation process in order to know exactly which was the port
selected.
