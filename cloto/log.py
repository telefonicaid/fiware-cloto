__author__ = 'gjp'
from configuration import LOGGING_PATH
import logging
logger = logging.getLogger('RuleEngine')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGGING_PATH + '/RuleEngine.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s policymanager.cloto [-] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
