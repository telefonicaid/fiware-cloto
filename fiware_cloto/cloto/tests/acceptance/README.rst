# FIWARE Scalability Manager and FIWARE Facts Acceptance Tests

Folder for acceptance tests of the FIWARE Scalability Manager & FIWARE Facts.

## Content of the acceptance tests

The acceptance tests are divided into 3 different groups:

- rules, contain the core of the acceptance tests to manage the operation related to rules management over the component.

- subscription, contain the operation related to management of subscriptions to a new server.

- tenant_information, keep the different operations related to the management of tenant information and window management.

You can find them under `fiware_cloto/cloto/tests/acceptance/component` folder.

## How to Run the Acceptance Tests

### Prerequisites:

- Python 2.7 or newer

- pip installed (http://docs.python-guide.org/en/latest/starting/install/linux/)

- virtualenv installed (pip install virtalenv)

- Git installed (yum install git-core / apt-get install git)

### Environment preparation:

- Create a virtual environment somewhere, e.g. in ENV (virtualenv ENV)

- Activate the virtual environment (source ENV/bin/activate)

- Change to the tests/acceptance folder of the project

- Install the requirements for the acceptance tests in the virtual environment:


     pip install -r requirements.txt --allow-all-external.


- Configure file in `fiware_cloto/cloto/tests/acceptance/commons/configuration.py` 
  adding the keystone url, and a valid user, password and tenant ID.

### Tests execution:

- Change to the `fiware_cloto/cloto/tests/acceptance` folder of the project if not already on it.

- Run behave with appropriate params (see available ones with the -h option), by default you can launch them just executing
     
     behave
