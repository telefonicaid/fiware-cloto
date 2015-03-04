#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
__author__ = 'gjp'
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized, InternalServerError
from cloto.models import TokenModel
import json
import requests
from cloto.constants import ACCEPT_HEADER, JSON_TYPE, X_AUTH_TOKEN_HEADER, TOKENS_PATH, SERVICE_NOT_AUTORIZED, \
    TOKEN_NOT_FOUND


class AuthorizationManager():
    """This class provides methods to manage authorization.
    """
    myClient = None
    client = requests

    def generate_adminToken(self, username, password, url):
        """This method generates an admin token."""
        try:
            admin_client = self.myClient.Client(username=username, password=password, auth_url=url)
            return admin_client.auth_token
        except AuthorizationFailure as auf:
            raise(auf)
        except Unauthorized as unauth:
            raise(unauth)

    def checkToken(self, admin_token, token, tenant_id, url):
        """checks if a token is valid against a url using an admin token."""
        print("Starting Authentication of token %s " % token)
        try:
            if not token:
                raise Unauthorized("Token is empty")
            auth_result = self.get_info_token(url, admin_token, token)
            if auth_result:
                if tenant_id == auth_result.tenant["id"]:
                    print('The token is valid')
                else:
                    raise Unauthorized("Token is not valid for specified tenant %s" % tenant_id)
        except Unauthorized as unauth:
            raise unauth
        except InternalServerError as internalError:
            raise AuthorizationFailure("Token could not have enough permissions to access tenant: %s" % tenant_id)
        except Exception as ex:
            raise ex

    def get_info_token(self, url, admin_token, token):
        headers = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: admin_token}
        r = self.client.get(url + "/" + TOKENS_PATH + token, headers=headers)
        response = r.text.decode()
        if response == TOKEN_NOT_FOUND:
            raise AuthorizationFailure(response)
        if response == SERVICE_NOT_AUTORIZED:
            raise AuthorizationFailure("System has an authorization problem, please ask to administrators.")
        info = json.loads(response)
        my_token = TokenModel()
        my_token.expires = info["access"]["token"]["expires"]
        my_token.id = info["access"]["token"]["id"]
        my_token.tenant = info["access"]["token"]["tenant"]
        return my_token
