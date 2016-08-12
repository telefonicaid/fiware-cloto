Changelog
=========

v2.7.0 (2016-08-12)
-------------------

New
~~~

- Use Orion v1 API

Changes
~~~~~~~

- Update docker files
- Update documentation

Fix
~~~
- Fix problem in settings file

v2.6.0 (2016-06-27)
-------------------
New
~~~

- Create docker files. [Henar Muñoz]

Changes
~~~~~~~

- Migrate E2E tests to behave tool. [Fernando Lopez]
- Refactoring utils content. [Henar Muñoz]
- Update property file. [Henar Muñoz]
- Update documentation. [Fernando Lopez]

Fix
~~~

- Add automatic version renumbering. [Fernando Lopez]
- Remove explicit IP in the component. [Guillermo Jimenez Prieto]

v2.5.0 (2016-04-01)
-------------------

New
~~~

- Add Jenkins config files to utils directory. [Guillermo Jimenez
  Prieto]

- Add new tests related to restCloto authentication. [Guillermo Jimenez
  Prieto]

- Add new SECURITY LEVEL to define when user tokens should be checked
  against keystone. [Guillermo Jimenez Prieto]

- User Tokens are now stored in memory to decrease the number of
  requests to keystone. [Guillermo Jimenez Prieto]

- Remove migrations from coverage report. [Guillermo Jimenez Prieto]

Changes
~~~~~~~

- Refactor and new tests to check tokens stored in memory. [Guillermo
  Jimenez Prieto]

- Update Readme file with a better explanation about MYSQL PATH.
  [Guillermo Jimenez Prieto]

- Fix coverage report using coverage util. [Guillermo Jimenez Prieto]

- Update Readme with new installation order according to new django
  version. [Guillermo Jimenez Prieto]

- Update  django version to improve security system. [Guillermo Jimenez
  Prieto]

v2.4.0 (2016-02-10)
-------------------

New
~~~

- New resource to show server information without authentication.
  [Guillermo Jimenez Prieto]

Changes
~~~~~~~

- Adding version constant to setup.py instead of an imported Version to
  prevent failures during pip installation. [Guillermo Jimenez Prieto]

Fix
~~~

- Adding default values to configuration if configuration file does not
  exists or is not provided. [Guillermo Jimenez Prieto]

v2.3.0 (2015-12-29)
-------------------

Fix
~~~

- Fixing keystone client import using v3. [Guillermo Jimenez Prieto]

v2.2.0 (2015-12-23)
-------------------

New
~~~

- Adding new test to cover the bug fixed. [Guillermo Jimenez Prieto]

- Adding new test to cover the bug fixed. [Guillermo Jimenez Prieto]

- Adding information and utils to run fiware cloto with supervisor.
  [Guillermo Jimenez Prieto]

Changes
~~~~~~~

- Removing skip tag from acceptance scenario after fixing the bug
  CLAUDIA-5703. [Guillermo Jimenez Prieto]

Fix
~~~

- Fixing email notification. [Guillermo Jimenez Prieto]

- Fixed string response code. [Guillermo Jimenez Prieto]

- Fixed string response code. [Guillermo Jimenez Prieto]

- Fixed json notification when email notification is launched.
  [Guillermo Jimenez Prieto]

- Fixing logger info when some valid numeric string is updating a
  windowsize. [Guillermo Jimenez Prieto]

- Fixing exception block to catch error when some string is updating a
  windowsize. [Guillermo Jimenez Prieto]

v2.1.0 (2015-11-11)
-------------------

Fix
~~~

- Fixing mkdir error if folder already exists. [Guillermo Jimenez
  Prieto]

- Fixing CI travis build when any test fails. [Guillermo Jimenez Prieto]

v2.0.0 (2015-10-23)
-------------------

New
~~~

- Adding tests to check environment cleaning. [Guillermo Jimenez Prieto]

- Cleaning environments before creating the new ones. [Guillermo Jimenez
  Prieto]

- New unit test to check fail connection while windowsize updating.
  [Guillermo Jimenez Prieto]

- XUnit report is now generated. [Guillermo Jimenez Prieto]

- Changed the way to execute unit tests, now it is performed as django
  recommends. [Guillermo Jimenez Prieto]

- Tests: new tests to check the windowsize update. [Guillermo Jimenez
  Prieto]

- Cloto sends windowsill updates to a rabbitmq in order to notify to
  fiware-facts. [Guillermo Jimenez Prieto]

Changes
~~~~~~~

- Version is now recovered from settings file. [Guillermo Jimenez
  Prieto]

Fix
~~~

- Fixing wrong logger import in wsgi file. [Guillermo Jimenez Prieto]

- Moving build to root folder. [Guillermo Jimenez Prieto]

- Fixing cobertura report publishing into sonar. [Guillermo Jimenez
  Prieto]

- Fixing sonar reports. [Guillermo Jimenez Prieto]

v1.8.0 (2015-09-29)
-------------------

New
~~~

- Server is now creating all tables when it starts. No more user
  interaction is needed. [Guillermo Jimenez Prieto]

- New installation for fiware-cloto using PIP. [Guillermo Jimenez
  Prieto]

- Improving configuration taking data from a configuration file located
  in /etc/fiware.d/fiware-cloto.cfg. [Guillermo Jimenez Prieto]

- Adding new files to the package data. [Guillermo Jimenez Prieto]

Fix
~~~

- Adding more useful information to documentation. [Guillermo Jimenez
  Prieto]

- Updating documentation according the new installation using PIP.
  [Guillermo Jimenez Prieto]

- Adding parent folder to sys environment to execute unit tests without
  errors with this new file distribution. [Guillermo Jimenez Prieto]

- Moving all files into a new module folder called fiware_cloto.
  [Guillermo Jimenez Prieto]

v1.7.1 (2015-09-08)
-------------------

Fix
~~~

- Updated apiary documentation in order to add new data. [Fernando]

v1.6.0 (2015-07-28)
-------------------

Fix
~~~

- Fixing missing badges on README file. [Guillermo Jimenez Prieto]

v1.5.0 (2015-05-29)
-------------------

New
~~~

- Develop the functionality to connect Policy Manager with Keystone
  using APIv3. [Guillermo Jimenez Prieto]

v1.4.0 (2015-03-03)
-------------------

New
~~~

- New unit tests and refactor of environment script. [Guillermo
  Jimenez Prieto]


v1.3.0 (2014-12-01)
-------------------

Changes
~~~~~~~

- Readme is now in RsT format. [Guillermo Jimenez Prieto]

Fix
~~~

- Fixing Acceptance Tests with all new cloto structure. [Guillermo
  Jimenez Prieto]

- Fixing logging from django files. [Guillermo Jimenez Prieto]

- Fixing cobertura report to work with jenkins and sonar. [Guillermo
  Jimenez Prieto]

v1.2.0 (2014-11-04)
-------------------

New
~~~

- Added CHANGELOG.rst file for fiware-cloto. [Guillermo Jimenez Prieto]

- Added CHANGELOG config file for gitchangelog. [Guillermo Jimenez
  Prieto]

- Settings are now in a single file fix: dev: Settings are now loaded
  correctly. [Guillermo Jimenez Prieto]

- Adding more unit tests. [Guillermo Jimenez Prieto]

- Allowed host added into automatic installer. Now default local IP
  address is added to settings.py. [Guillermo Jimenez Prieto]

- Adding documentation to github. [geonexus]

Changes
~~~~~~~

- Preparing release. (1.2.0) [Guillermo Jimenez Prieto]

- Removing developer's IP from ALLOWED HOSTS. [Guillermo Jimenez Prieto]

- Checkstyle fixes. [Guillermo Jimenez Prieto]

- Adding more unit tests. [Guillermo Jimenez Prieto]

- Indentation fix. [Guillermo Jimenez Prieto]

Fix
~~~

- Api info fixed to public wiki url and omit production settings from
  coverage. [Guillermo Jimenez Prieto]

- Pep8 fixes. [Guillermo Jimenez Prieto]

- More unit tests for wsgi. [Guillermo Jimenez Prieto]

- Skipping wsgi tests. [Guillermo Jimenez Prieto]

- Fixing not found error on travis. [Guillermo Jimenez Prieto]

- Adding white space between allowed hosts in settings file. [Guillermo
  Jimenez Prieto]

- Loggers are mocked in unittests. [Guillermo Jimenez Prieto]

- Added fail view for Mac Servers. [geonexus]

- Rules are now stored correctly. There was a bug that stores all rules
  with unicode values. [geonexus]

- Server version is now based on a string value and it is needed to
  change value in configuration.py before each release. [geonexus]

- Changing version float in server information to string value. Fixing
  some words mistaken. [geonexus]

- Adding HTTP TRACE TRACK methods disabling instructions. [geonexus]

- Adding PyClips requirement to README.md. [geonexus]

- Updating databases to mysql commands. [geonexus]

- Updating databases to mysql commands. [geonexus]

- Adding titles to rst files. [geonexus]

- Adding documentation to github. [geonexus]

- Adding documentation to github. [geonexus]

- Adding documentation to github. [geonexus]
