sed -i -e "s/{ADM_TENANT_NAME}/${ADM_TENANT_NAME}/" /etc/fiware.d/fiware-cloto.cfg
sed -i -e "s/{ADM_PASSWORD}/${ADM_PASSWORD}/" /etc/fiware.d/fiware-cloto.cfg
sed -i -e "s/{KEYSTONE_IP}/${KEYSTONE_IP}/" /etc/fiware.d/fiware-cloto.cfg
sed -i -e "s/{ADM_TENANT_ID}/${ADM_TENANT_ID}/" /etc/fiware.d/fiware-cloto.cfg
sed -i -e "s/{ADM_USERNAME}/${ADM_USERNAME}/" /etc/fiware.d/fiware-cloto.cfg
sed -i -e "s/{OS_USER_DOMAIN_NAME}/${OS_USER_DOMAIN_NAME}/" /etc/fiware.d/fiware-cloto.cfg

while ! nc -z mysql 3306; do sleep 8; done
python setup.py install
cd /
gunicorn fiware_cloto.cloto.wsgi -b 0.0.0.0
