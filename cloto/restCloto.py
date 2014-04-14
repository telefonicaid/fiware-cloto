__author__ = 'gjp'
from django import http
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import json
import OrionClient
from cloto.manager import InfoManager, RuleManager, AuthorizationManager
from cloto.models import TenantInfo
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized, Conflict
from keystoneclient.v2_0 import client
import datetime
from json import JSONEncoder
from configuration import OPENSTACK_URL, ADM_USER, ADM_PASS


class RESTResource(object):
    """
    Dispatches based on HTTP method.
    """
    # Possible methods; subclasses could override this.
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    info = None

    def __call__(self, request, *args, **kwargs):
        callback = getattr(self, request.method, None)
        if callback:
            try:
                a = AuthorizationManager.AuthorizationManager()
                a.myClient = client
                adm_token = a.generate_adminToken(ADM_USER, ADM_PASS, OPENSTACK_URL)
                a.checkToken(adm_token, request.META['HTTP_X_AUTH_TOKEN'],
                             kwargs.get("tenantId"), OPENSTACK_URL)
                return callback(request, *args, **kwargs)
            except AuthorizationFailure as auf:
                return HttpResponse(json.dumps(
                    {"unauthorized": {"code": 401, "message": str(auf)}}, indent=4), status=401)
            except Unauthorized as unauth:
                return HttpResponse(json.dumps(
                    {"unauthorized": {"code": 401, "message": str(unauth)}}, indent=4), status=401)
            except ValueError as excep:
                return HttpResponse(json.dumps({"unauthorized": {"code": 401,
                                                                 "message": str(excep)}}, indent=4), status=401)
            except KeyError as excep:
                f = str(excep)
                if f.__contains__("HTTP_X_AUTH_TOKEN"):
                    return HttpResponse(json.dumps({"unauthorized": {"code": 401, "message":
                        "This server could not verify that you are authorized to access the document you requested."
                        " Either you supplied the wrong credentials (e.g., bad password), or your browser does not "
                        "understand how to supply the credentials required."}}, indent=4), status=401)

        else:
            allowed_methods = [m for m in self.methods if hasattr(self, m)]
            return http.HttpResponseNotAllowed(allowed_methods)

    def set_info(self, information):
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
            return HttpResponse(json.dumps({"serverId": serverId, "ruleId": rule.ruleId}, indent=4))
        except ValueError as err:
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
            return HttpResponse(json.dumps(vars(rule), indent=4))
        except ValueError as err:
            return HttpResponseBadRequest(json.dumps({"badRequest": {"code": 400, "message":
                        str(err)}}, indent=4))
        except KeyError as err:
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
            ruleManager.orionClient = OrionClient.OrionClient()
            subscriptionId = ruleManager.subscribe_to_rule(tenantId, serverId, request.body)
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
            ruleManager.orionClient = OrionClient.OrionClient()
            ruleManager.unsubscribe_to_rule(serverId, subscriptionId)
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
            ruleManager.orionClient = OrionClient.OrionClient()
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
