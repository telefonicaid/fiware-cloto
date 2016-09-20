=================================
 Welcome to Bosun Policy Manager
=================================

Introduction
============

Bosun is the reference implementation (GEri) of FIWARE Policy Manager GE, and
its component Cloto provides a REST API to create rules associated to servers,
subscribe to Context Broker to get information about resources consumption of
those servers, and launch actions described in rules when conditions are met.

Policy Manager provides the basic management of cloud resources based on rules,
as well as management of the corresponding resources within the FIWARE Cloud
instance like actions based on physical monitoring or infrastructure, security
monitoring of resources and services or whatever that could be defined by facts,
actions and rules. Policy Manager is a easy rule engine designed to be used in
the OpenStack ecosystem and, of course, inside the FIWARE Cloud.

IMPORTANT NOTE: This GE reference implementation product is only of interest
to potential FIWARE instance providers and therefore has been used to build
the basic FIWARE platform core infrastructure of FIWARE Lab. If you are an
application developer, you don't need to create a complete FIWARE instance
locally in order to start building applications based on FIWARE. You may rely
on instances of FIWARE GEris linked to the Data/Media Context Management, the
IoT Services Enablement and the Advanced Web-based User Interface chapters, or
some GEris of the Applications/Services Ecosystem and Delivery Framework chapter
(WireCloud) as well as the Security chapter (Access Control). Those instances
are either global instances or instances you can create on FIWARE Lab, but also
instances you may create by downloading, installing and configuring the
corresponding software in your own premises.  

Bosun Policy Manager REST API source code can be found here__.

__ `FIWARE Cloto GitHub Repository`_


Documentation
=============

GitHub's README__ provides a good documentation summary, and the following
cover more advanced topics:

__ `FIWARE Cloto GitHub README`_


.. title:: Home

.. toctree::
   :maxdepth: 1

   user_guide
   admin_guide
   architecture
   open_spec

.. REFERENCES

.. _FIWARE Cloto GitHub Repository: https://github.com/telefonicaid/fiware-cloto.git
.. _FIWARE Cloto GitHub README: https://github.com/telefonicaid/fiware-cloto/blob/master/README.rst
