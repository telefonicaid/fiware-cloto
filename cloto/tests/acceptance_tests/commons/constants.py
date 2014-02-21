__author__ = 'artanis'


LITTLE_SLEEP = 1

#INFORMATION RESPONSE CONSTANTS

TENANT_OWNER = u'owner'
TENANT_WSIZE = u'windowsize'
TENANT_DOC = u'doc'
TENANT_VERSION = u'version'

CONTENT_TYPE_HEADER = u'content-type'
DEFAULT_CONTENT_TYPE_HEADER = u'application/json'
AUTHENTICATION_HEADER = u'X-Auth-Token'

SERVER_ID = u'serverId'

RULE_NAME = u'name'
RULE_CONDITION = u'condition'
RULE_ACTION = u'action'
RULE_ID = u'ruleId'
RULE_URL = u'url'
RULE_CONDITION_DEFAULT = u'?serv <- (server (server-id ?x) (cpu ?y&:(< ?y 30)) (mem ?z) (hdd ?t))'
RULE_ACTION_DEFAULT = u'assert (alertCPU ?x))(python-call env-call-rest-api)'
LONG_NAME = u'This is a long name to test the maximum length of elasticity rule'
