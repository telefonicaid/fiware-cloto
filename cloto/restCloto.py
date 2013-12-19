__author__ = 'gjp'
from django import http
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import json
import information
from cloto.manager import InfoManager, RuleManager
from cloto.models import TenantInfo
from django.core import serializers


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
            return callback(request, *args, **kwargs)
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
            self.set_info(info)
            return HttpResponse(json.dumps(self.info.getVars(), indent=4))
        except Exception as err:
            print err.message
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            self.set_info(information.information(tenantId))
            return HttpResponse(json.dumps(self.info.getVars(), indent=4))
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
                return HttpResponse(json.dumps(vars(list(t.items)), indent=4))
                # return HttpResponse("OK. windowsize updated to %s." % info2.windowsize)
            else:
                return HttpResponseBadRequest("Bad Request. windowsize could not be parsed")
        except Exception as err:
            t = TenantInfo(tenantId=tenantId, windowsize=5)
            t.save()
            self.set_info(information.information(tenantId))
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
        rule = RuleManager.RuleManager().create_general_rule(tenantId, request.body)

        return HttpResponse(json.dumps(rule.getVars(), indent=4))


class ServersGeneralView(RESTResource):
    """
    Servers general view PATH( /v1.0/{tenantID}/servers/ ).
    """
    def GET(self, request, tenantId):
        h = HttpResponse("Should return a list of servers with their rules")
        h.status_code = 501
        return h


class ServerView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/ ).
    """
    def GET(self, request, tenantId, serverId):
        h = HttpResponse("Should return a list of all rules of server %s" % serverId)
        h.status_code = 501
        return h

    def PUT(self, request, tenantId, serverId):
        h = HttpResponse("Should update the context of server %s" % serverId)
        h.status_code = 501
        return h


class ServerRulesView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/rules/ ).
    """
    def GET(self, request, tenantId, serverId):
        h = HttpResponse("Should return a list of all rules of server %s" % serverId)
        h.status_code = 501
        return h

    def POST(self, request, tenantId, serverId):
        ruleId = RuleManager.RuleManager().create_specific_rule(tenantId, serverId, request.body)
        return HttpResponse(json.dumps({"serverId": serverId, "ruleId": str(ruleId)}, indent=4))

    def PUT(self, request, tenantId, serverId, ruleId):
        h = HttpResponse("Should update the rule condition of server %s" % serverId)
        h.status_code = 501
        return h

    def DELETE(self, request, tenantId, serverId, ruleId):
        h = HttpResponse("Should delete the rule associated to server %s" % serverId)
        h.status_code = 501
        return h

    def GET(self, request, tenantId, serverId, ruleId):
        h = HttpResponse("Should return the specified rule of server %s" % serverId)
        h.status_code = 501
        return h


class JSONResponse(http.HttpResponse):
    """This class serializes data into a json HttpResponse.
    """
    def __init__(self, data):
        mime = "application/json"
        super(JSONResponse, self).__init__(
            content=json.dumps(data, sort_keys=True),
            mimetype=mime,
        )

import datetime
from json import JSONEncoder


class DateEncoder(JSONEncoder):
    """This class helps to serialize datetime attributes in order to return it as json response.
    """
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)
