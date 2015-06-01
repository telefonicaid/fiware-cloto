Changelog
=========

v1.5.0 (2015-05-29)
------------------

New
~~~

- Develop the functionality to connect Policy Manager with Keystone
  using APIv3. [Guillermo Jimenez Prieto]

v1.4.0 (2015-03-03)
------------------

New
~~~

- New unit tests and refactor of environment script. [Guillermo
  Jimenez Prieto]


v1.3.0 (2014-12-01)
------------------

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
