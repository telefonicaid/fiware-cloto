User & Programmers Guide
________________________

.. contents:: :local:

Introduction
============

Welcome the User and Programmer Guide for the Policy Manager Generic
Enabler. The online documents are being continuously updated and
improved, and so will be the most appropriate place to get the most up
to date information on using this interface.

Please go to GitHub's `README <https://github.com/telefonicaid/fiware-cloto/blob/master/README.rst>`_ for more
documentation.

Background and Detail
---------------------

This User and Programmers Guide relates to the Policy Manager GE which
is part of the `Cloud Hosting Chapter`_. Please find more information
about this Generic Enabler in the following `Open Specification`_.

User Guide
==========

The Policy Manager GE is a backend component, without user interface.
Therefore there is no need to provide a user guide. The Cloud Portal can
be used for Web-based interaction (but it is not part of this GE).

Programmer Guide
================

Policy Manager API is based upon HTTP and therefore all devices, which
can handle HTTP traffic, are possible clients.

Accessing Policy Manager from the CLI
-------------------------------------

To invoke the REST API use the curl program. Curl `[1] <http://curl.haxx.se/>`_
is a client to get documents/files from or send documents to a server, using any
of the supported protocols (HTTP, HTTPS, FTP, LDAP, FILE, etc.) and therefore is
also suitable for Policy Manager API. Use either the curl command line tool or
libcurl from within your own programs in C. Curl is free and open software
that compiles and runs under a wide variety of operating systems.

In order to make a probe of the different functionalities related to the
Policy Manager, we make a list of several operations to make a probe of
the execution of these GEis.

**1. Get a valid token for the tenant that we have (It is not a Policy
Manager operation but a IdM operation).**

Due to all operations of the Policy Manager are using the security
mechanism which is used in the rest of the cloud component, it is needed
to provide a security token in order to continue with the rest of
operations.

::

    curl -d '{"auth": {"tenantName": $TENANT, "passwordCredentials":{"username": $USERNAME,
    "password": $PASSWORD}}}' -H "Content-type: application/json"
    -H "Accept: application/xml"  http://$KEYSTONE_HOST:$KEYSTONE_PORT/v2.0/tokens

Both $TENANT (Project), $USERNAME and $PASSWORD must be values
previously created in the OpenStack Keystone. The IP address
$KEYSTONE_HOST and the Port $KEYSTONE_PORT are the data of our internal
installation of IdM, if you planned to execute it you must changed it by
the corresponding IP and Port of the FIWARE Keystone or IdM IP and Port
addresses.

We obtained two data from the previous sentence:

-  X-Auth-Token

::

    <token expires="2012-10-25T16:35:42Z" id="a9a861db6276414094bc1567f664084d">

-  Tenant-Id

::

    <tenant enabled="true" id="c907498615b7456a9513500fe24101e0" name=$TENANT>

**2. Get tenant information**

This is the first real operation about our GEi, by which we can obtain
the information about the Policy Manager, together with the information
about the window size fixed for the execution of the GEi. For more
information about the window size and its meaning.

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d'
    -X GET http://<RULE ENGINE HOST>:8000/v1.0/c907498615b7456a9513500fe24101e0

This operation will return the information regarding the tenant details
of the execution of the Policy Manager

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 08:25:17 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8
    {
        "owner": "Telefonica I+D", 
        "doc": "http://docs.policymanager.apiary.io",
        "runningfrom": "14/04/09 07:45:22", 
        "version": 1.0, 
        "windowsize": 10
    }

**3. Create a rule for a server**

This operation allows to create a specific rule associate to a server:

::

    curl -v -H 'X-Auth-Token: 86e096cd4de5490296fd647e21b7f0b4'
    -X POST http://130.206.81.71:8000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers
    /32c23ac4-230d-42b6-81f2-db9bd7e5b790/rules/
    -d '{"action": {"actionName": "notify-scale", "operation": "scaleUp"}, "name": "ScaleUpRule",
    "condition": { "cpu": { "value": 98, "operand": "greater" },
    "mem": { "value": 95, "operand": "greater equal"}}}'

The result of this operation is the following content:

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 10:14:11 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8
    {
        "serverId": "32c23ac4-230d-42b6-81f2-db9bd7e5b790", 
        "ruleId": "68edb416-bfc6-11e3-a8b9-fa163e202949"
    }

**4. Subscribe the server to the rule**

Through this operation we can subscribe a rule to be monitored in order
to evaluate the rule to be processed.

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d'
    -X POST http://130.206.81.71:8000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers
    /32c23ac4-230d-42b6-81f2-db9bd7e5b790/subscription
    -d '{ "ruleId": "ruleid", "url": "URL to notify any action" }'

An the expected result is the following.

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 10:16:11 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8
    {
        "serverId": "32c23ac4-230d-42b6-81f2-db9bd7e5b790", 
        "subscriptionId": "6f231936-bfce-11e3-9a13-fa163e202949"
    }

**5. Manual simulation of data transmission to the server**

This operation simulate the operation that the context broker used to
send data to the Policy Manager, the normal execution of this process
will be automatically once that the Policy Manager subscribes a rule to
a specific server. The operation is related to fiware-facts component and
it has the following appearance:

::

    curl -v -H "Content-Type: application/json"
    -X POST http://127.0.0.1:5000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers/serverI1
    -d '{
    "contextResponses": [
        {
            "contextElement": {
               "attributes": [
                   {
                       "value": "0.12",
                       "name": "usedMemPct",
                       "type": "string"
                   },
                   {
                       "value": "0.14",
                       "name": "cpuLoadPct",
                       "type": "string"
                   },
                   {
                       "value": "0.856240",
                       "name": "freeSpacePct",
                       "type": "string"
                   },
                   {
                       "value": "0.8122",
                       "name": "netLoadPct",
                       "type": "string"
                   }
               ],
               "id": "Trento:193.205.211.69",
               "isPattern": "false",
               "type": "host"
           },
           "statusCode": {
               "code": "200",
               "reasonPhrase": "OK"
           }
       }]
    }'

Which produces the following result after the execution:

::

    * About to connect() to 127.0.0.1 port 5000 (#0)
    *   Trying 127.0.0.1...
    * Adding handle: conn: 0x7fa2e2804000
    * Adding handle: send: 0
    * Adding handle: recv: 0
    * Curl_addHandleToPipeline: length: 1
    * - Conn 0 (0x7fa2e2804000) send_pipe: 1, recv_pipe: 0
    * Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
    > POST /v1.0/33/servers/44 HTTP/1.1
    > User-Agent: curl/7.30.0
    > Host: 127.0.0.1:5000
    > Accept: */*
    > Content-Type: application/json
    > Content-Length: 1110
    > Expect: 100-continue
    > 
    < HTTP/1.1 100 Continue
    < HTTP/1.1 200 OK
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 0
    < Date: Wed, 09 Apr 2014 00:11:49 GMT
    < 
    * Connection #0 to host 127.0.0.1 left intact

**6. Unsubscribe the previous rule**

In order to stop the process to evaluate rules, it is needed to
unsubscribe the activated rule. We can do it with the following
operation:

::

    curl -v -H 'X-Auth-Token: a9a861db6276414094bc1567f664084d'
    -X DELETE http://130.206.81.71:8000/v1.0/6571e3422ad84f7d828ce2f30373b3d4/servers
    /serverI1/subscription/SubscriptionId

::

    < HTTP/1.0 200 OK
    < Date: Wed, 09 Apr 2014 10:16:59 GMT
    < Server: WSGIServer/0.1 Python/2.6.6
    < Content-Type: text/html; charset=utf-8

	
Accessing Policy Manager from a browser
---------------------------------------

To send HTTP requests to Policy Manager using a browser, you may use:

- Chrome browser `[2] <http://www.google.es/chrome?platform=linux&hl=en-GB>`_
  with the Simple REST Client plugin `[3]
  <https://chrome.google.com/webstore/detail/fhjcajmcbmldlhcimfajhfbgofnpcjmb>`_
- Firefox RESTClient add-on `[4]
  <https://addons.mozilla.org/en-US/firefox/addon/restclient/>`_.


.. REFERENCES

.. _Cloud Hosting Chapter: https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Cloud_Hosting_Architecture
.. _Open Specification: https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/FIWARE.OpenSpecification.Cloud.PolicyManager
