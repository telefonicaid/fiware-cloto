from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


@csrf_exempt
def some_page(request):

    if request.method == 'POST':
        return HttpResponse("Mira mi POST")
    elif request.method == 'GET':
        return HttpResponse("Mira mi GET")
    else:
        raise Http404()


@csrf_protect
def test(request):
    return HttpResponse("Mira mi Test")
    print("test")


@csrf_protect
def test(request):
    return HttpResponse("Mira mi Test de POST")
    print("test")


@csrf_protect
def test(request):
    return HttpResponse("Mira mi Test de GET")
    print("test")


def fail(request, reason="csrf fails"):
    print("csrf token failed")
