__author__ = 'fla'

# cobertura dir must be in the root of our project not django
COBERTURA_DIR = join('target', 'site', 'cobertura')
UNIT_TESTS_DIR = join('target', 'surefire-reports')
if not exists(COBERTURA_DIR):
    makedirs(COBERTURA_DIR)

if not exists(UNIT_TESTS_DIR):
    makedirs(UNIT_TESTS_DIR)

NOSE_ARGS = ['-s',
             '-v',
             '--cover-erase',
             '--cover-branches',
             '--with-cov',
             '--cover-package=books,commons,users',
             '--cover-xml',
             '--cover-xml-file={0}/coverage.xml'.format(COBERTURA_DIR),
             '--with-xunit',
             '--xunit-file={0}/TEST-nosetests.xml'.format(UNIT_TESTS_DIR)
             ]