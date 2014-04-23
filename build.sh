# File to execute the covertura and unit test and generate the information
# to be shown in sonar
#
# __author__ = 'fla'

virtualenv ENV
source ENV/bin/activate
mkdir /var/log/fiware-cloto
chmod 777 /var/log/fiware-cloto
pip install -r requirements.txt
python manage.py syncdb
python manage.py test cloto --settings=settings.jenkins
deactivate

