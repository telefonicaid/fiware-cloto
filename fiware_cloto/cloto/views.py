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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from fiware_cloto.cloto.manager import InfoManager
from django.core.exceptions import ObjectDoesNotExist
import json


@csrf_exempt
def info(request):
    try:
        info = InfoManager.InfoManager().get_information()
        return HttpResponse(json.dumps(info.getVars(), indent=4))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"badRequest": {"code": 500, "message":
                            "Server Database does not contain information server"}}, indent=4), status=500)


def fail(request, reason="csrf fails"):
    return HttpResponse("csrf fails", status=400)
