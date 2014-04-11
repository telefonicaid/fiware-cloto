__author__ = 'gjp'


# OPENSTACK CONFIGURATION
OPENSTACK_URL = u'http://130.206.80.61:35357/v2.0'
ADM_USER = u''
ADM_PASS = u''

# POLICY MANAGER CONFIGURATION
DEFAULT_WINDOW_SIZE = 5
OWNER = u'Telefonica I+D'
API_INFO_URL = u'https://forge.fi-ware.org/plugins/mediawiki/wiki/fi-ware-private/' \
               u'index.php/FIWARE.OpenSpecification.Details.Cloud.PolicyManager'
VERSION = 1.0
MAX_WINDOW_SIZE = 10
LOGGING_PATH = u'/var/log/fiware-cloto'
RABBITMQ_URL = u'localhost'

ENVIRONMENTS_MANAGER_PATH = u'cloto/environmentManager.py'
ENVIRONMENTS_PATH = u'cloto/environment.py'
CLIPS_PATH = u'cloto/clips'

# ORION CONTEXT BROKER CONFIGURATION
CONTEXT_BROKER_URL = u'http://130.206.81.57:1026/NGSI10'
NOTIFICATION_URL = u'http://130.206.81.71:5000/v1.0'
NOTIFICATION_TYPE = u'ONTIMEINTERVAL'
NOTIFICATION_TIME = u'PT5S'
