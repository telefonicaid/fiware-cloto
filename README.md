fiware-cloto
============
[![Build Status](https://travis-ci.org/geonexus/fiware-cloto.svg)](https://travis-ci.org/geonexus/fiware-cloto)
[![Coverage Status](https://coveralls.io/repos/geonexus/fiware-cloto/badge.png?branch=develop)](https://coveralls.io/r/geonexus/fiware-cloto?branch=develop)

FIWARE Cloud Scalability Manager - Cloto


### Description
-----------
This module is part of FI-WARE Policy Manager. It provides an API-REST for create rules associated to servers,
subscribe servers to Context Broker to get information about resources consumption of that servers and launch actions
described in rules when conditions are given.


### Prerequisites:
------------
To install this module you have to install some components:

- Python 2.7
- Apache 2.2 or above + mod_wsgi
- RabbitMQ Server
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)


### Installation
------------
Once you have all prerequisites installed, run install.sh with sudo privileges in order to start installation.
This script should install fiware-cloto in /opt/policyManager

After finishing you must configure cloto configuration and some apache settings.


### Configuration - Cloto
---------------------

Before starting the rule engine, you should edit configuration.py located at cloto folder.
Constants you need to complete are:

    - All in # OPENSTACK CONFIGURATION: Openstack information
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

