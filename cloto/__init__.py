import sqlite3
import datetime
from models import ServerInfo
from django.utils import timezone
from configuration import OWNER, API_INFO_URL, VERSION
from circus import get_arbiter
from circus.process import Process
import time


conn = sqlite3.connect('cloto.db')
c = conn.cursor()
runningfrom = datetime.datetime.now(tz=timezone.get_default_timezone())
# Creating initial data

try:
    s = ServerInfo(id=1, owner=OWNER, version=VERSION, runningfrom=runningfrom, doc=API_INFO_URL)
    s.save()
    print ("data was inserted")
except Exception as err:
    print("Tables already exists: %s" % err)

# Save (commit) the changes.
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

arbiter = get_arbiter([{"cmd": "python cloto/environmentManager.py", "numprocesses": 1}], background=True)
arbiter.start()
