#!/bin/sh
# File to install fiware-cloto into the system
#
# __author__ = 'gjp'

if [ "$(whoami)" != "root" ]; then
    echo "Sorry, try to install fiware-cloto using root."
    exit 1
fi

echo "Installing fiware-cloto on system..."

installation_path="/opt/policyManager/fiware-cloto"
config_file="fiware-cloto.cfg"
config_path="/etc/sysconfig/$config_file"


log_path="/var/log/fiware-cloto"

if [ ! -d "$log_path" ]; then
  mkdir -m 777 $log_path
  echo 0 > $log_path/RuleEngine2.log
fi

echo "..."

#cp settings/fiware-cloto.cfg $config_path

if [ ! -d "$installation_path" ]; then
  mkdir -p $installation_path
fi

echo "..."

cp -r * /opt/policyManager/fiware-cloto/
chmod 777 /opt/policyManager/fiware-cloto/
cd /opt/policyManager/fiware-cloto/
ln fiware-cloto /etc/init.d/fiware-cloto
chmod a+x /etc/init.d/fiware-cloto

echo "..."
pip install -r requirements.txt
python manage.py syncdb
echo "..."
echo "...Done"
echo "Please check file located in $1 to configure all parameters before start fiware-cloto"
echo "### To execute fiware-cloto run file run.sh ###"
