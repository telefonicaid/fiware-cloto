__author__ = 'gjp'
from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import json
import information
from cloto.manager import InfoManager, RuleManager, AuthorizationManager
from cloto.models import TenantInfo
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized
from keystoneclient.v2_0 import client
import datetime
from json import JSONEncoder


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
                adm_token = a.generate_adminToken("admin", "openstack", "http://130.206.80.61:35357/v2.0")
                a.checkToken(adm_token, request.META['HTTP_X_AUTH_TOKEN'],
                             kwargs.get("tenantId"), "http://130.206.80.61:35357/v2.0")
                return callback(request, *args, **kwargs)
            except AuthorizationFailure as auf:
                return HttpResponse("The request you have made requires authentication or Token could not have enough "
                                    "permissions to access tenant: %s" % kwargs.get("tenantId"), status=401)
            except Unauthorized as unauth:
                return HttpResponse("You have to provide a valid token: %s" % unauth.message, status=401)
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
            #self.set_info(info)
            return HttpResponse(json.dumps(info.getVars(), indent=4))
        except ObjectDoesNotExist as err:
            print err.message
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            info = InfoManager.InfoManager().get_information(tenantId)
            #self.set_info(information.information(tenantId))
            return HttpResponse(json.dumps(info.getVars(), indent=4))
            # return HttpResponseServerError(err.message)

    def PUT(self, request, tenantId):
        try:
            # here we should call to MongoDB in order to get the information

            info = InfoManager.InfoManager().get_information(tenantId)
            self.set_info(info)
            info2 = self.info.parse(request.body)
            if info2 != None:
                # here we must update MongoDB's windowsize with data received.
                t = InfoManager.InfoManager().updateWindowSize(tenantId, info2.windowsize)
                return HttpResponse(json.dumps({"windowsize": info2.windowsize}, indent=4))
               # return HttpResponse(json.dumps(vars(list(t.items)), indent=4))
                # return HttpResponse("OK. windowsize updated to %s." % info2.windowsize)
            else:
                return HttpResponseBadRequest("Bad Request. windowsize could not be parsed")
        except ObjectDoesNotExist as err:
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            info = InfoManager.InfoManager().get_information(tenantId)
            self.set_info(info)
            info2 = self.info.parse(request.body)
            #self.set_info(information.information(tenantId))
            t = InfoManager.InfoManager().updateWindowSize(tenantId, info2.windowsize)
            return HttpResponse(json.dumps({"windowsize": info2.windowsize}, indent=4))
            # return HttpResponse(json.dumps(vars(info2)))
            # return HttpResponse("OK. windowsize updated to %s." % info2.windowsize)


class GeneralRulesViewRule(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/rules/{ruleId} ).
    """

    def GET(self, request, tenantId, ruleId):
        try:
            rule = RuleManager.RuleManager().get_rule(ruleId)
            return HttpResponse(json.dumps(rule.getVars(), indent=4))
            #return JSONResponse(rule.getVars())
        except ObjectDoesNotExist as err:
            return HttpResponse("Rule %s does not exists" % ruleId, status=404)
        except Exception as err:
            return HttpResponseServerError(err.message)

    def PUT(self, request, tenantId, ruleId):
        #rule = RuleManager.RuleManager().update_Rule(ruleId, request.body)
        #return HttpResponse(json.dumps(rule.getVars(), indent=4))

        h = HttpResponse("Should update a general rule")
        h.status_code = 501
        return h

    def DELETE(self, request, tenantId, ruleId):
        try:
            RuleManager.RuleManager().delete_rule(ruleId)
            return HttpResponse()
        except Exception as err:
            return HttpResponseServerError(err.message)


class GeneralRulesView(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/rules/ ).
    """

    def GET(self, request, tenantId):
        try:
            rules = RuleManager.RuleManager().get_all_rules(tenantId)
            return HttpResponse(json.dumps(vars(rules), cls=DateEncoder, indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)

    def POST(self, request, tenantId):
        try:
            rule = RuleManager.RuleManager().create_general_rule(tenantId, request.body)
            return HttpResponse(json.dumps(rule.getVars(), indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)


class ServersGeneralView(RESTResource):
    """
    Servers general view PATH( /v1.0/{tenantID}/servers/ ).
    """
    def GET(self, request, tenantId):
        try:
            entities = RuleManager.RuleManager().get_all_entities(tenantId)
            return HttpResponse(json.dumps(vars(entities), cls=DateEncoder, indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)

        h = HttpResponse("Should return a list of servers with their rules")
        h.status_code = 501
        return h


class ServerView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/ ).
    """
    def GET(self, request, tenantId, serverId):
        try:
            rules = RuleManager.RuleManager().get_all_specific_rules(tenantId, serverId)
            return HttpResponse(json.dumps(vars(rules), cls=DateEncoder, indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)

    def PUT(self, request, tenantId, serverId):
        h = HttpResponse("Should update the context of server %s" % serverId)
        h.status_code = 501
        return h


class ServerRulesView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/rules/ ).
    """
    def POST(self, request, tenantId, serverId):
        try:
            ruleId = RuleManager.RuleManager().create_specific_rule(tenantId, serverId, request.body)
            return HttpResponse(json.dumps({"serverId": serverId, "ruleId": str(ruleId)}, indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)

    def PUT(self, request, tenantId, serverId, ruleId):
        h = HttpResponse("Should update the rule condition of server %s" % serverId)
        h.status_code = 501
        return h

    def DELETE(self, request, tenantId, serverId, ruleId):
        try:
            RuleManager.RuleManager().delete_specific_rule(serverId, ruleId)
            return HttpResponse()
        except ObjectDoesNotExist as err:
            return HttpResponse("Rule %s does not exists" % ruleId, status=404)
        except Exception as err:
            return HttpResponseServerError(err.message)

    def GET(self, request, tenantId, serverId, ruleId):
        #h = HttpResponse("Should return the specified rule of server %s" % serverId)
        #h.status_code = 501
        #return h
        try:
            rule = RuleManager.RuleManager().get_specific_rule(ruleId)
            return HttpResponse(json.dumps(vars(rule), cls=DateEncoder, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse("Rule %s does not exists" % ruleId, status=404)
        except Exception as err:
            return HttpResponseServerError(err.message)


class ServerSubscriptionView(RESTResource):
    """
    Subscription view PATH( /v1.0/{tenantID}/servers/{serverId}/subscription/ ).
    """
    def POST(self, request, tenantId, serverId):
        try:
            subscriptionId = RuleManager.RuleManager().subscribe_to_rule(tenantId, serverId, request.body)
            return HttpResponse(json.dumps({"serverId": serverId, "subscriptionId": str(subscriptionId)}, indent=4))
        except Exception as err:
            return HttpResponseServerError(err.message)

    def DELETE(self, request, tenantId, serverId, subscriptionId):
        try:
            RuleManager.RuleManager().unsubscribe_to_rule(tenantId, serverId, subscriptionId)
            return HttpResponse()
        except ObjectDoesNotExist as err:
            return HttpResponse("Subscription %s does not exists" % subscriptionId, status=404)
        except Exception as err:
            return HttpResponseServerError(err.message)

    def GET(self, request, tenantId, serverId, subscriptionId):
        #h = HttpResponse("Should return the specified rule of server %s" % serverId)
        #h.status_code = 501
        #return h
        try:
            rule = RuleManager.RuleManager().get_subscription(tenantId, serverId, subscriptionId)
            return HttpResponse(json.dumps(vars(rule), cls=DateEncoder, indent=4))
        except ObjectDoesNotExist as err:
            return HttpResponse("Subscription %s does not exists" % subscriptionId, status=404)
        except Exception as err:
            return HttpResponseServerError(err.message)


class DateEncoder(JSONEncoder):
    """This class helps to serialize datetime attributes in order to return it as json response.
    """
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)
