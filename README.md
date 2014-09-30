fiware-cloto
============
[![Build Status](https://travis-ci.org/telefonicaid/fiware-cloto.svg)](https://travis-ci.org/telefonicaid/fiware-cloto)
[![Coverage Status](https://coveralls.io/repos/telefonicaid/fiware-cloto/badge.png)](https://coveralls.io/r/telefonicaid/fiware-cloto)
[![PyPi version](https://pypip.in/v/cloto/badge.png)](https://crate.io/packages/cloto/)
[![PyPi license](https://pypip.in/license/cloto/badge.png)](https://crate.io/packages/cloto/)

FIWARE Cloud Scalability Manager - Cloto


### Description
-----------
This module is part of FI-WARE Policy Manager. It provides an API-REST to create rules associated to servers,
subscribe servers to Context Broker to get information about resources consumption of that servers and launch actions
described in rules when conditions are given.


### Prerequisites:
------------
To install this module you have to install some components:

- Python 2.7
- Apache 2.2 or above + mod_wsgi
- RabbitMQ Server
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)


### Installation
------------

Once you have all prerequisites installed, you must create a DB named cloto in your MySQL server.
In addition, be sure you have installed mysql-devel package for development of MySQL applications.
You should be able to install it from yum or apt-get package managers.
    examples: yum install mysql-devel
              apt-get install mysql-devel
              ...etc

After all  you must run install.sh with sudo privileges in order to start installation.
This script should install fiware-cloto in /opt/policyManager and it will ask you for some configuration
parameters, please, ensure you have all this data before starting the script in order to install fiware-cloto
easiest.
    - Keystone URL.
    - Keystone admin user, password and tenant.
    - Mysql user and password.

After finishing you must configure cloto configuration and some apache settings.


### Configuration - Cloto
---------------------

Before starting the rule engine, you should edit configuration.py located at cloto folder.
Constants you need to complete are:

    - All in # OPENSTACK CONFIGURATION: Openstack information (If you provide this information in the install
    script you do not need to edit)
    - RABBITMQ_URL: URL Where RabbitMQ is listening (no port needed, it uses default port)
    - CONTEXT_BROKER_URL: URL where Context Broker is listening
    - NOTIFICATION_URL: URL where notification service is listening (This service must be implemented by the user)

in addition you could modify other constants like NOTIFICATION_TIME, or DEFAULT_WINDOW_SIZE.

Finally you should modify ALLOWED_HOSTS parameter in settings.py adding the hosts you want to be accesible from outside,
 your IP address, the domain name, etc. An example could be like this:

    ALLOWED_HOSTS = ['policymanager.host.com','80.71.123.2’]


### Configuration - Apache + wsgi
-----------------------------
Edit your httpd.conf file and add:

    WSGIScriptAlias / PATH_TO_fiware-cloto/cloto/wsgi.py
    WSGIPythonPath PATH_TO_fiware-cloto

    <Directory PATH_TO_fiware-cloto/cloto>
        <Files wsgi.py>
            Order deny,allow
            Allow from all
        </Files>
    </Directory>
    <Directory PATH_TO_fiware-cloto>
        <Files cloto.db>
            Allow from all
        </Files>
    </Directory>
    <Directory /var/log/fiware-cloto>
        <Files RuleEngine.log>
            Allow from all
        </Files>
    </Directory>

Note that PATH_TO_fiware-cloto should be: /opt/policyManager/fiware-cloto

Finally you sould add cloto port to this httpd.conf file

    Listen 8000


### Running fiware-cloto
--------------------

To run fiware-cloto, just execute:

    service fiware-cloto start

To stop fiware-cloto, execute:

    service fiware-cloto stop

