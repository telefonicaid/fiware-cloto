__author__ = 'gjp'
from django import http
from django.http import HttpResponse, HttpResponseBadRequest
import json
from cloto import information


class RESTResource(object):
    """
    Dispatches based on HTTP method.
    """
    # Possible methods; subclasses could override this.
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __call__(self, request, *args, **kwargs):
        callback = getattr(self, request.method, None)
        if callback:
            return callback(request, *args, **kwargs)
        else:
            allowed_methods = [m for m in self.methods if hasattr(self, m)]
            return http.HttpResponseNotAllowed(allowed_methods)


class GeneralView(RESTResource):
    """
    General Operations PATH( /v1.0/{tenantID}/ ).
    """
    def GET(self, request, tenantId):
        info = information.information()
        return JSONResponse(vars(info))

    def PUT(self, request, tenantId):
        # here we should call to MongoDB in order to get the information
        info = information.information()

        # here we must update MongoDB's windowsize with data received.
        info = info.parse(request.body)
        if (info != None):
            return HttpResponse("OK. windowsize updated to %s." % info.windowsize)
        else:
            return HttpResponseBadRequest("Bad Request. windowsize could not be parsed")


class ServersGeneralView(RESTResource):
    """
    Servers general view PATH( /v1.0/{tenantID}/servers/ ).
    """
    def GET(self, request, id):
        return HttpResponse("Testing server GET")

    def PUT(self, request, id):
        return HttpResponse("Testing update context")


class ServersView(RESTResource):
    """
    Servers view PATH( /v1.0/{tenantID}/servers/{serverId}/ ).
    """
    def GET(self, request, id):
        return HttpResponse("Testing GET")

    def DELETE(self, request, id):
        return HttpResponse("Testing delete")

    def PUT(self, request, id):
        return HttpResponse("Testing PUT")


class JSONResponse(http.HttpResponse):
    def __init__(self, data):
        mime = "application/json"
        super(JSONResponse, self).__init__(
            content=json.dumps(data, sort_keys=True),
            mimetype=mime,
        )
