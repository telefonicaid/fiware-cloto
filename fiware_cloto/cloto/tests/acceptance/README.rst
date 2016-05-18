.. _Top:
========================================================
FIWARE Bosun (Policy Manager GE): Cloto Acceptance Tests
========================================================

Folder for acceptance tests of the FIWARE Bosun (Policy Manager GE): Cloto Acceptance Tests.

Content of the acceptance tests
===============================

The acceptance tests are divided into 3 different groups:

- rules, contain the core of the acceptance tests to manage the operation related to rules management over the component. The features that are included in this set are the following:

.. code::

    create_rule.feature
    delete_rule.feature
    list_rules_server.feature
    list_servers.feature
    retrieve_rule.feature

- subscription, contain the operation related to management of subscriptions to a new server. This is compound with the following features:

.. code::

    create_subscription.feature
    delete_subscription.feature
    retrieve_subscription.feature
    update_rule.feature

- tenant_information, keep the different operations related to the management of tenant information and window management.  This is compound with the following features:

.. code::

    retrieve_tenant_information.feature
    update_windowsize.feature


You can find them under `fiware_cloto/cloto/tests/acceptance/component/features` folder.

Top_.

How to Run the Acceptance Tests
===============================

Requirements
------------

- Python 2.7 or newer

- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)

- virtualenv installed (pip install virtalenv)

- Git installed (yum install git-core / apt-get install git)

Top_.

Environment execution
---------------------

Previously to the preparation and execution of the acceptance tests, you should have an complete instance 
of the FIWARE Bosun:Cloto up and running in some place in order to check the acceptance tests. You have the 
posibility to follow the indications of the installation of the component in the README file or you can use 
the preconfigured docker that we have prepared to run the acceptance tests.

Keep in mind that you need to have an access to a OpenStack Keystone instance to tackle with the identity 
management.

To start deployment the docker, you have to follow the following steps

- Firstly,  you need to specify the following environment variables:

.. code::

    $ export KEYSTONE_IP=<IP of a Keystone instance>
    $ export ADM_TENANT_ID=<ID of the administration tenant to be used>
    $ export USER_TENANT_ID=<ID of the user tenant id used in the test>
    $ export ADM_TENANT_NAME=<admin tenant name>
    $ export USER_TENANT_NAME=<user tenant name>
    $ export ADM_USERNAME=<admin name>
    $ export USER_USERNAME=<user name>
    $ export ADM_PASSWORD=<admin password>
    $ export USER_PASSWORD=<user password>

- Create the proper docker image if you do not yet it. You can find the docker file Dockerfile_cloto in the `docker` folder

.. code::

    $ docker build -t fiware-cloto -f Dockerfile_cloto .

- Finally, launch the docker compose of the Cloto component:

.. code:: 

    $ docker-compose -f docker-compose-develop.yml up -d

Top_.

Environment preparation
-----------------------

- Create a virtual environment somewhere, e.g. in ENV (virtualenv ENV)

- Activate the virtual environment (source ENV/bin/activate)

- Change to the tests/acceptance folder of the project

- Install the requirements for the acceptance tests in the virtual environment:

.. code::

     $ pip install -r requirements.txt --allow-all-external.


- Configure file in `fiware_cloto/cloto/tests/acceptance/commons/configuration.py` 
  adding the keystone url, and a valid user, password and tenant ID.

Top_.

Tests execution
---------------

- Change to the `fiware_cloto/cloto/tests/acceptance` folder of the project if not already on it.

- Run behave with appropriate params (see available ones with the -h option), by default you can launch them just executing

.. code::

     $ behave

Top_.
