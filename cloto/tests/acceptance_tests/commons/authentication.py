__author__ = 'arobres'

import requests


def get_token():
    body = '{"auth": {"tenantName": "admin", "passwordCredentials":{"username": "admin", "password": "2 b @bl3 2 3nt3r"}}}'
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    url = 'http://130.206.80.61:35357/v2.0/tokens'
    r = requests.request(method='post', url=url, data=body, headers=headers)
    response = r.json()
    token_id = response['access']['token']['id']
    tenant_id = response['access']['token']['tenant']['id']
    return token_id, tenant_id
