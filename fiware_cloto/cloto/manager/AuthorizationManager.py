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
import json
import re

from keystoneclient.exceptions import AuthorizationFailure, Unauthorized, InternalServerError
import requests
from keystoneclient import session
from fiware_cloto.cloto.models import TokenModel
from fiware_cloto.cloto.utils.log import logger
from fiware_cloto.cloto.constants import ACCEPT_HEADER, JSON_TYPE, X_AUTH_TOKEN_HEADER, TOKENS_PATH_V2, \
    DEFAULT_REQUEST_TIMEOUT, X_SUBJECT_TOKEN_HEADER, TOKENS_PATH_V3, HTTP_RESPONSE_CODE_OK, AUTH_API_V2, AUTH_API_V3,\
    AUTH_TOKEN_ERROR_MESSAGE
from django.conf import settings
from django.utils import timezone, dateparse


class AuthorizationManager():
    """This class provides methods to manage authorization.
    """
    myClient = None
    client = requests
    session = None
    auth_token = None
    api_version = None
    identity_url = None

    user_tokens = {}

    def __init__(self, identity_url, api_version):
        """
        Default contructor.
        :param identity_url: The url of the Keystone service.
        :param api_version: The version of the Kesytone API to be used.
        :return: None
        """
        self.session = session

        if api_version == AUTH_API_V2:
            from keystoneclient.v2_0 import client as keystone_client
        elif api_version == AUTH_API_V3:
            from keystoneclient.v3 import client as keystone_client
        else:
            msg = 'The allowed values for api version are {} or {}'.format(AUTH_API_V2, AUTH_API_V3)
            raise ValueError(msg)

        self.myClient = keystone_client
        self.api_version = api_version
        self.identity_url = identity_url

    def get_auth_token(self, username, password, tenant_id, **kwargs):
        """
        Init the variables related to authorization, needed to execute tests
        :return: The auth token retrieved
        """
        if self.auth_token is None:

            cred_kwargs = {
                'auth_url': self.identity_url,
                'username': username,
                'password': password
            }

            # Currently, both v2 and v3 Identity API versions are supported
            if self.api_version == AUTH_API_V2:
                cred_kwargs['tenant_name'] = kwargs.get('tenant_name')
            elif self.api_version == AUTH_API_V3:
                cred_kwargs['user_domain_name'] = kwargs.get('user_domain_name')

            # Instantiate a Password object
            try:
                identity_package = 'keystoneclient.auth.identity.%s' % self.api_version.replace('.0', '')
                identity_module = __import__(identity_package, fromlist=['Password'])
                password_class = getattr(identity_module, 'Password')
                logger.debug("Authentication with %s", password_class)
                credentials = password_class(**cred_kwargs)
            except (ImportError, AttributeError) as e:
                    raise e
            # Get auth token
            logger.debug("Getting auth token for tenant %s...", tenant_id)
            try:
                auth_sess = self.session.Session(auth=credentials, timeout=DEFAULT_REQUEST_TIMEOUT)
                self.auth_token = auth_sess.get_token()
                logger.debug("Admin token generated: %s", self.auth_token)

            except Exception as e:
                logger.error("No auth token (%s)", e.message)
                raise(e)

        return self.auth_token

    def get_token_from_memory(self, token):
        """Get token information from Dictionary stored in memory containing all valid user tokens used previously"""
        return self.user_tokens[token]

    def checkToken(self, admin_token, token, tenant_id):
        """checks if a token is valid against a url using an admin token."""

        token_db = None
        try:
            if not token:
                raise Unauthorized("Token is empty")
            logger.debug("Starting Authentication of token %s ", token)

            try:
                token_db = self.get_token_from_memory(token)
                if self.api_version == AUTH_API_V2:
                    time_to_review = token_db['createdAt'] + timezone.timedelta(
                        seconds=int(settings.SECURITY_LEVEL_SECONDS_V2[settings.SECURITY_LEVEL]))
                elif self.api_version == AUTH_API_V3:
                    time_to_review = token_db['createdAt'] + timezone.timedelta(
                        seconds=int(settings.SECURITY_LEVEL_SECONDS_V3[settings.SECURITY_LEVEL]))

                logger.debug("Token {0} is present in memory, should be checked at {1}".format(token, time_to_review))
                expires = dateparse.parse_datetime(token_db['expires'])
                if timezone.now() > expires or timezone.now() > time_to_review or tenant_id is not token_db["tenant"]:
                    logger.debug("Token %s should be checked against keystone.", token)
                else:
                    return token
            except KeyError:

                logger.debug("Token %s is not present in DB", token)
                pass

            auth_result = self.get_info_token(admin_token, token)
            if auth_result:
                if tenant_id == auth_result.tenant["id"]:
                    # STORE TOKEN IN MEMORY
                    createdAt = timezone.now()
                    token_db = self.user_tokens.setdefault(token, {'id': auth_result.id, 'expires': auth_result.expires,
                                                                 'username': auth_result.username,
                                                                 'tenant': auth_result.tenant["id"],
                                                                 'createdAt': createdAt})

                    self.user_tokens[token] = token_db
                    return token

                else:
                    logger.error("TenantId %s ", tenant_id)
                    logger.error("Token TenantId %s ", auth_result.tenant["id"])
                    raise Unauthorized("Token is not valid for specified tenant %s" % tenant_id)

        except AuthorizationFailure as ex:
            if re.search(self.auth_token, ex.message) or re.search(AUTH_TOKEN_ERROR_MESSAGE, ex.message):
                self.auth_token = None
                logger.debug("Admin token has expired, setting global to None.")
            elif re.search(token, ex.message) and token_db:
                self.user_tokens.pop(token)
            raise ex
        except Unauthorized as unauth:
            logger.debug(unauth)
            raise unauth
        except InternalServerError as internalError:
            raise AuthorizationFailure("Token could not have enough permissions to access tenant: %s" % tenant_id)
        except Exception as ex:
            raise ex

    def get_info_token(self, admin_token, token):
        """ Gets the token details and return a TokenModel with that information
        :param admin_token: the auth token needed to get token information
        :param token: the token which information will be taken
        :return: TokenModel with the information.
        """

        if self.api_version == AUTH_API_V2:
            headers = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: admin_token}
            r = self.client.get(self.identity_url + "/" + TOKENS_PATH_V2 + token, headers=headers)

            if r.status_code != HTTP_RESPONSE_CODE_OK or r.text == "User token not found" \
                    or r.text == "Service not authorized":
                raise AuthorizationFailure(r.text)
            response = r.text.decode()
            info = json.loads(response)
            tmp = info["access"]["token"]
            my_token = TokenModel(expires=tmp["expires"], id=tmp["id"],
                                  username=info["access"]["user"]["username"], tenant=tmp["tenant"])

        elif self.api_version == AUTH_API_V3:
            headers = {ACCEPT_HEADER: JSON_TYPE, X_AUTH_TOKEN_HEADER: admin_token, X_SUBJECT_TOKEN_HEADER: token}
            r = self.client.get(self.identity_url + "/" + TOKENS_PATH_V3, headers=headers)
            response = r.text.decode()
            if r.status_code is not HTTP_RESPONSE_CODE_OK:
                raise AuthorizationFailure(response)
            info = json.loads(response)
            tmp = info["token"]
            my_token = TokenModel(expires=tmp["expires_at"], id=token, username=tmp['user']['name'],
                                  tenant=tmp["project"])

        return my_token
