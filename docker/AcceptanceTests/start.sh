sed -i -e "s/{USER_PASSWORD}/${USER_PASSWORD}/" commons/configuration.py
sed -i -e "s/{KEYSTONE_IP}/${KEYSTONE_IP}/" commons/configuration.py
sed -i -e "s/{USER_TENANT_NAME}/${USER_TENANT_NAME}/" commons/configuration.py
sed -i -e "s/{USER_TENANT_ID}/${USER_TENANT_ID}/" commons/configuration.py
sed -i -e "s/{USER_USERNAME}/${USER_USERNAME}/" commons/configuration.py
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
while ! nc -z fiwarecloto 8000; do sleep 8; done
behave component/features --tags ~@skip --junit --junit-directory testreport
