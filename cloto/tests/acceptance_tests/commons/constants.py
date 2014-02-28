__author__ = 'artanis'


LITTLE_SLEEP = 1

#INFORMATION RESPONSE CONSTANTS

TENANT_OWNER = u'owner'
TENANT_WSIZE = u'windowsize'
TENANT_DOC = u'doc'
TENANT_VERSION = u'version'
TENANT_KEY = u'tenantId'

CONTENT_TYPE_HEADER = u'content-type'
DEFAULT_CONTENT_TYPE_HEADER = u'application/json'
AUTHENTICATION_HEADER = u'X-Auth-Token'

SERVER_ID = u'serverId'

RULE_NAME = u'name'
RULE_CONDITION = u'condition'
RULE_ACTION = u'action'
RULE_ID = u'ruleId'
RULE_SPECIFIC_ID = u'specificRule_Id'
RULE_URL = u'url'
RULE_CONDITION_DEFAULT = u'?serv <- (server (server-id ?x) (cpu ?y&:(< ?y 30)) (mem ?z) (hdd ?t))'
RULE_ACTION_DEFAULT = u'assert (alertCPU ?x))(python-call env-call-rest-api)'
RULE_URL_DEFAULT = u'http://localhost:8080/notify'
LONG_NAME = u'This is a long name to test the maximum length of elasticity rule'
RULES = u'rules'
SERVERS = u'servers'

SUBSCRIPTION_ID = u'subscriptionId'


RANDOM = u'random'
DEFAULT = u'default'

ITEM_NOT_FOUND_ERROR = u'itemNotFound'

#DB_TABLES

DB_SPECIFIC_RULES = u'cloto_specificrule'
DB_SUBSCRIPTION = u'cloto_subscription'
DB_ENTITY_SPECIFIC_RULES = u'cloto_entity_specificrules'
DB_ENTITY_SUBSCRIPTION = u'cloto_entity_subscription'
DB_CLOTO_ENTITY = u'cloto_entity'
DB_RULE_AND_SUBSCRIPTION = (DB_SPECIFIC_RULES, DB_SUBSCRIPTION, DB_ENTITY_SUBSCRIPTION, DB_ENTITY_SPECIFIC_RULES,
                            DB_CLOTO_ENTITY)
