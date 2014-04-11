import sqlite3
import datetime

from django.utils import timezone
from circus import get_arbiter

from models import ServerInfo
from configuration import OWNER, API_INFO_URL, VERSION, ENVIRONMENTS_MANAGER_PATH
from configuration import CONTEXT_BROKER_URL, NOTIFICATION_URL, LOGGING_PATH
from cloto.log import logger


conn = sqlite3.connect('cloto.db')
c = conn.cursor()
runningfrom = datetime.datetime.now(tz=timezone.get_default_timezone())
# Creating initial data
try:
    s = ServerInfo(id=1, owner=OWNER, version=VERSION, runningfrom=runningfrom, doc=API_INFO_URL)
    s.save()
except Exception as err:
    logger.warn("DataBase already exists: %s" % err)

# Save (commit) the changes.
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

arbiter = get_arbiter([{"cmd": "python "+ ENVIRONMENTS_MANAGER_PATH, "numprocesses": 1}], background=True)
#arbiter.start()
logger.info("SERVER STARTED")
