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
from django.core.exceptions import ImproperlyConfigured
from django.core.servers.basehttp import get_internal_wsgi_application
from django.core.wsgi import get_wsgi_application
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils import six


class WSGITest(TestCase):
    urls = "fiware_cloto.cloto.urls"

    @override_settings(WSGI_APPLICATION="fiware_cloto.cloto.wsgi.application")
    def test_get_wsgi_application(self):
        """
        Verify that ``get_wsgi_application`` returns a functioning WSGI callable.
        """
        application = get_wsgi_application()
        environ = RequestFactory()._base_environ(
            PATH_INFO="/info",
            CONTENT_TYPE="text/html; charset=utf-8",
            REQUEST_METHOD="GET"
            )
        response_data = {}

        def start_response(status, headers):
            response_data["status"] = status
            response_data["headers"] = headers
        response = application(environ, start_response)
        self.assertEqual(response_data["status"], "500 Internal Server Error")
        self.assertEqual(
            response_data["headers"],
            [('Content-Type', 'text/html; charset=utf-8')])
        self.assertEqual(
            bytes(response),
            b'Content-Type: text/html; charset=utf-8\r\n\r\n{\n   '
            b' "badRequest": {\n       '
            b' "message": "Server Database does not contain information server", \n '
            b'       "code": 500\n    }\n}')


class GetInternalWSGIApplicationTest(TestCase):

    @override_settings(WSGI_APPLICATION="fiware_cloto.cloto.wsgi.application")
    def test_success(self):
        """
        If ``WSGI_APPLICATION`` is a dotted path, the referenced object is
        returned.
        """
        app = get_internal_wsgi_application()
        from fiware_cloto.cloto.wsgi import application
        self.assertTrue(app is application)

    @override_settings(WSGI_APPLICATION=None)
    def test_default(self):
        """
        If ``WSGI_APPLICATION`` is ``None``, the return value of
        ``get_wsgi_application`` is returned.
        """
        # Mock out get_wsgi_application so we know its return value is used
        fake_app = object()

        def mock_get_wsgi_app():
            return fake_app

        from django.core.servers import basehttp
        _orig_get_wsgi_app = basehttp.get_wsgi_application
        basehttp.get_wsgi_application = mock_get_wsgi_app
        try:
            app = get_internal_wsgi_application()
            self.assertTrue(app is fake_app)
        finally:
            basehttp.get_wsgi_application = _orig_get_wsgi_app

    @override_settings(WSGI_APPLICATION="fiware_cloto.cloto.wsgi.noexist.app")
    def test_bad_module(self):
        with six.assertRaisesRegex(self,
            ImproperlyConfigured,
            r"WSGI application 'fiware_cloto.cloto.wsgi.noexist.app' could not be loaded; Error importing module: "
            r"'No module named noexist'"):
            get_internal_wsgi_application()

    @override_settings(WSGI_APPLICATION="fiware_cloto.cloto.wsgi.noexist")
    def test_bad_name(self):
        with six.assertRaisesRegex(self,
            ImproperlyConfigured,
            r"WSGI application 'fiware_cloto.cloto.wsgi.noexist' could not be loaded; Error importing module:"
            r" 'Module \"fiware_cloto.cloto.wsgi\" does not define a \"noexist\" attribute/class'"):
            get_internal_wsgi_application()
