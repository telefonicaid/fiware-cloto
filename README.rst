FIWARE Policy Manager GE
____________________


| |Build Status| |Coverage Status| |Pypi Version| |Pypi License|


Description
===========

This module is part of FIWARE Policy Manager. It provides an API-REST to create rules associated to servers,
subscribe servers to Context Broker to get information about resources consumption of that servers and launch actions
described in rules when conditions are given.

For more information, please refer to the `documentation <doc/README.rst>`_.


Prerequisites
=============
To install this module you have to install some components:

- Python 2.7
- PyClips 1.0 (http://sourceforge.net/projects/pyclips/files/)
- Apache 2.2 or above + mod_wsgi
- RabbitMQ Server 3.3.0 or above (http://www.rabbitmq.com/download.html)
- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)
- MySQL 5.6.14 or above (http://dev.mysql.com/downloads/mysql/)
- gcc-c++ and gcc libraries


Installation
============

Once you have all prerequisites installed, you must create a DB named cloto in your MySQL server.
Ensure your mysql path is in your path. If not, you can add executing (change /usr/local/ with your mysql folder):
    export PATH=$PATH:/usr/local/mysql/bin

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


Configuration - Cloto
=====================
Before starting the rule engine, you should edit settings.py located at cloto folder or in /etc/sysconfig/fiware-cloto.cfg.
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


Configuration - Apache + wsgi
=============================
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

We recommend you to disable HTTP TRACK|TRACE methods adding to httpd.conf TraceEnable directive
and set the value to Off

    TraceEnable Off


Running fiware-cloto
====================

To run fiware-cloto, just execute:

    service fiware-cloto start

To stop fiware-cloto, execute:

    service fiware-cloto stop


License
=======

\(c) 2013-2014 Telefónica I+D, Apache License 2.0


.. IMAGES

.. |Build Status| image:: https://travis-ci.org/telefonicaid/fiware-cloto.svg?branch=develop
   :target: https://travis-ci.org/telefonicaid/fiware-cloto
.. |Coverage Status| image:: https://coveralls.io/repos/telefonicaid/fiware-cloto/badge.png?branch=develop
   :target: https://coveralls.io/r/telefonicaid/fiware-cloto
.. |Pypi Version| image:: https://pypip.in/v/fiware-cloto/badge.png
   :target: https://pypi.python.org/pypi/fiware-cloto/
.. |Pypi License| image:: https://pypip.in/license/fiware-cloto/badge.png
   :target: https://pypi.python.org/pypi/fiware-cloto/
