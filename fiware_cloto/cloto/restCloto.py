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
from fiware_cloto.orion_wrapper import orion_client

__author__ = 'gjp'
from django import http
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import json
from fiware_cloto.cloto.constants import HTTP_RESPONSE_CODE_UNAUTHORIZED, AUTH_API_V3, AUTH_API_V2
from fiware_cloto.cloto.manager import RuleManager, AuthorizationManager, InfoManager
from fiware_cloto.cloto.models import TenantInfo
from fiware_cloto.cloto.utils.log import logger
from keystoneclient.exceptions import Conflict, AuthorizationFailure

import datetime
from json import JSONEncoder
from django.conf import settings


class RESTResource(object):
    """
    Dispatches based on HTTP method.
    """
    # Possible methods; subclasses could override this.
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    info = None
    a = AuthorizationManager.AuthorizationManager(settings.OPENSTACK_URL, settings.AUTH_API)

    def __call__(self, request, *args, **kwargs):
        """Starting point of the API Agent. All REST requests should enter through this method.
        """
        callback = getattr(self, request.method, None)
        if callback:

            try:
                if self.a.auth_token is None:
                    self.a.get_auth_token(settings.ADM_USER, settings.ADM_PASS, settings.ADM_TENANT_ID,
                                                  tenant_name=settings.ADM_TENANT_NAME,
                                             user_domain_name=settings.USER_DOMAIN_NAME)
                self.a.checkToken(self.a.auth_token, request.META['HTTP_X_AUTH_TOKEN'],
                             kwargs.get("tenantId"))
                return callback(request, *args, **kwargs)
            except AuthorizationFailure as excep:
                if self.a.auth_token == None:
                    self.a.get_auth_token(settings.ADM_USER, settings.ADM_PASS, settings.ADM_TENANT_ID,
                                                  settings.OPENSTACK_URL,
                                                  tenant_name=settings.ADM_TENANT_NAME,
                                             user_domain_name=settings.USER_DOMAIN_NAME)
                    self.a.checkToken(self.a.auth_token, request.META['HTTP_X_AUTH_TOKEN'],
                             kwargs.get("tenantId"))
                    return callback(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps(
                        {"unauthorized": {"code": HTTP_RESPONSE_CODE_UNAUTHORIZED, "message": str(excep)}}, indent=4),
                        status=HTTP_RESPONSE_CODE_UNAUTHORIZED)

            except Exception as excep:
                return HttpResponse(json.dumps(
                    {"unauthorized": {"code": HTTP_RESPONSE_CODE_UNAUTHORIZED, "message": str(excep)}}, indent=4),
                    status=HTTP_RESPONSE_CODE_UNAUTHORIZED)

        else:
            allowed_methods = [m for m in self.methods if hasattr(self, m)]
            return http.HttpResponseNotAllowed(allowed_methods)

    def set_info(self, information):
        """Sets information generated about server.
        """
        self.info = information


class GeneralView(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/ ).
    """
    def GET(self, request, tenantId):
        try:
            info = InfoManager.InfoManager().get_information(tenantId)
            return HttpResponse(json.dumps(info.getVars(), indent=4))
        except ObjectDoesNotExist as err:
            print str(err)
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            info = InfoManager.InfoManager().get_information(tenantId)
            return HttpResponse(json.dumps(info.getVars(), indent=4))

    def PUT(self, request, tenantId):
        try:
            info = InfoManager.InfoManager().get_information(tenantId)
            self.set_info(info)
            info2 = self.info.parse(request.body)
            if info2 != None:
                t = InfoManager.InfoManager().updateWindowSize(tenantId, info2.windowsize)
                logger.debug("Window size updated for tenant: %s", tenantId)
                return HttpResponse(json.dumps({"windowsize": info2.windowsize}, indent=4))
            else:
                return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        "windowsize could not be parsed"}}, indent=4))
        except ObjectDoesNotExist as err:
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            info = InfoManager.InfoManager().get_information(tenantId)
            self.set_info(info)
            info2 = self.info.parse(request.body)
            t = InfoManager.InfoManager().updateWindowSize(tenantId, info2.windowsize)
            return HttpResponse(json.dumps({"windowsize": info2.windowsize}, indent=4))
        except ValidationError as ex:
                return HttpResponse(json.dumps({"badRequest": {"code": 400, "message":
                    ex.messages[0]}}, indent=4), status=400)
        except ValueError as ex:
                return HttpResponse(json.dumps({"badRequest": {"code": 400, "message":
                    ex.message}}, indent=4), status=400)


class GeneralRulesViewRule(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/rules/{ruleId} ).
    """

    def GET(self, request, tenantId, ruleId):
        try:
            rule = RuleManager.RuleManager().get_rule(ruleId)
            return HttpResponse(json.dumps(vars(rule), indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 400, "message":
                        "Rule %s does not exists" % ruleId}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def PUT(self, request, tenantId, ruleId):
        try:
            rule = RuleManager.RuleManager().update_rule(tenantId, ruleId, request.body)
            logger.debug("Rule updated: %s", ruleId)
            return HttpResponse(json.dumps(vars(rule), indent=4))
        except ValueError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def DELETE(self, request, tenantId, ruleId):
        try:
            RuleManager.RuleManager().delete_rule(ruleId)
            logger.debug("Rule deleted: %s", ruleId)
            return HttpResponse()
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))


class GeneralRulesView(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/rules/ ).
    """

    def GET(self, request, tenantId):
        try:
            rules = RuleManager.RuleManager().get_all_rules(tenantId)
            return HttpResponse(json.dumps(vars(rules), cls=DateEncoder, indent=4))
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def POST(self, request, tenantId):
        try:
            rule = RuleManager.RuleManager().create_general_rule(tenantId, request.body)
            logger.debug("Rule created: %s", rule.ruleId)
            return HttpResponse(json.dumps(vars(rule), indent=4))
        except ValueError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))


class ServersGeneralView(RESTResource):
    """
    Servers general view PATH( /v1.0/{tenantID}/servers/ ).
    """
    def GET(self, request, tenantId):
        #Should return a list of servers with their rules
        try:
            entities = RuleManager.RuleManager().get_all_entities(tenantId)
            return HttpResponse(json.dumps(vars(entities), cls=DateEncoder, indent=4))
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))


class ServerView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/ ).
    """
    def GET(self, request, tenantId, serverId):
        try:
            rules = RuleManager.RuleManager().get_all_specific_rules(tenantId, serverId)
            return HttpResponse(json.dumps(vars(rules), cls=DateEncoder, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def PUT(self, request, tenantId, serverId):
        # Should update the context of server
        #nfacts = myFactManager.insertFact(tenantId, serverId, request.body, arbiter)
        return HttpResponse(json.dumps({"OK": {"code": 200, "message":
                        "Should update the context of server %s" % serverId}}, indent=4))

        return HttpResponseServerError(json.dumps({"notImplemented": {"code": 501, "message":
                        "Should update the context of server %s" % serverId}}, indent=4))


class ServerRulesView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/rules/ ).
    """

    def POST(self, request, tenantId, serverId):
        try:
            rule = RuleManager.RuleManager().create_specific_rule(tenantId, serverId, request.body)
            logger.debug("Rule created: %s", rule.ruleId)
            return HttpResponse(json.dumps({"serverId": serverId, "ruleId": rule.ruleId}, indent=4))
        except ValueError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except ValidationError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except KeyError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except AttributeError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except TypeError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))


class ServerRuleView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/rules/{ruleId} ).
    """
    def PUT(self, request, tenantId, serverId, ruleId):
        try:
            rule = RuleManager.RuleManager().update_specific_rule(tenantId, serverId, ruleId, request.body)
            logger.debug("Rule updated: %s", ruleId)
            return HttpResponse(json.dumps(vars(rule), indent=4))
        except ValueError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except ValidationError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except KeyError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except AttributeError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except TypeError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def DELETE(self, request, tenantId, serverId, ruleId):
        try:
            RuleManager.RuleManager().delete_specific_rule(tenantId, serverId, ruleId)
            logger.debug("Rule deleted: %s", ruleId)
            return HttpResponse()
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def GET(self, request, tenantId, serverId, ruleId):
        # Should return the specified rule of server
        try:
            rule = RuleManager.RuleManager().get_specific_rule(tenantId, serverId, ruleId)
            return HttpResponse(json.dumps(vars(rule), cls=DateEncoder, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                str(err)}}, indent=4))


class ServerSubscriptionView(RESTResource):
    """
    Subscription view PATH( /v1.0/{tenantID}/servers/{serverId}/subscription/ ).
    """
    def POST(self, request, tenantId, serverId):
        try:
            ruleManager = RuleManager.RuleManager()
            ruleManager.orionClient = orion_client.orion_client()
            subscriptionId = ruleManager.subscribe_to_rule(tenantId, serverId, request.body)
            logger.debug("Subscrition created %s for server: %s", subscriptionId, serverId)
            return HttpResponse(json.dumps({"serverId": serverId, "subscriptionId": str(subscriptionId)}, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                        str(err)}}, indent=4), status=404)
        except Conflict as err:
            return HttpResponse(json.dumps({"conflict": {"code": 409, "message":
                        err.message}}, indent=4), status=409)
        except ValidationError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        err.messages[0]}}, indent=4))
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def DELETE(self, request, tenantId, serverId, subscriptionId):
        try:
            ruleManager = RuleManager.RuleManager()
            ruleManager.orionClient = orion_client.orion_client()
            ruleManager.unsubscribe_to_rule(serverId, subscriptionId)
            logger.debug("Subscription deleted %s for server: %s", subscriptionId, serverId)
            return HttpResponse()
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                        str(err)}}, indent=4))

    def GET(self, request, tenantId, serverId, subscriptionId):
        # Should return the specified rule of server
        try:
            ruleManager = RuleManager.RuleManager()
            ruleManager.orionClient = orion_client.orion_client()
            rule = ruleManager.get_subscription(tenantId, serverId, subscriptionId)
            return HttpResponse(json.dumps(vars(rule), cls=DateEncoder, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse(json.dumps({"itemNotFound": {"code": 404, "message":
                str(err)}}, indent=4), status=404)
        except Exception as err:
            return HttpResponseServerError(json.dumps({"serverFault": {"code": 500, "message":
                str(err)}}, indent=4))


class DateEncoder(JSONEncoder):
    """This class helps to serialize datetime attributes in order to return it as json response.
    """
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)
