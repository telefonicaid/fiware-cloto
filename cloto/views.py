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
