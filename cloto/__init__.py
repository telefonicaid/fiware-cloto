import sqlite3
import datetime
from models import ServerInfo
from django.utils import timezone


conn = sqlite3.connect('cloto.db')
c = conn.cursor()
owner = 'Telefonica I+D'
version = 1.0
runningfrom = datetime.datetime.now(tz=timezone.get_default_timezone())
doc = 'http://wikis.hi.inet/boi/index.php/Dinge_API'

# Creating initial Tables and initial data
try:
    c.execute('''CREATE TABLE cloto_entity_specificrules
             (specificRule_Id text, entity_Id text)''')
    c.execute('''CREATE TABLE cloto_specificrule
             (specificRule_Id text, tenantId text, name text, condition text, action text, createdAt datetime)''')
    c.execute('''CREATE TABLE cloto_entity
             (entity_Id text, tenantId text)''')
    c.execute('''CREATE TABLE cloto_serverinfo
             (id int, owner text, version real, runningfrom datetime, doc text, auth text)''')
    c.execute('''CREATE TABLE cloto_tenantinfo
             (id int, tenantId text, windowsize int, serverInfo_id int)''')
    c.execute('''CREATE TABLE cloto_rule
             (ruleId text, tenantId text, name text, condition text, action text, createdAt datetime)''')

    s = ServerInfo(id=1, owner=owner, version=version, runningfrom=runningfrom, doc=doc)
    s.save()
    print ("data was inserted")
except Exception as err:
    print("Tables already exists: %s" % err)
    myS = ServerInfo.objects.get(owner__contains=owner)
    myS.runningfrom = runningfrom
    myS.save()

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
