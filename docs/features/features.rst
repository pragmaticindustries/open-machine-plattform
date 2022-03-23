Features of the OMAP
====================

This page lists some important features of the OMAP platform.

User Management and Single-Sign-On
--------------

The platform uses Djangos well known `User Management <https://docs.djangoproject.com/en/4.0/topics/auth/default/#auth-admin>`_.
For production usage we recomment the usage of a more scalable solution like `Keycloak <https://www.keycloak.org/>`_.
Any OAuth2 capable provider is suitable but single-sign on is crucial when one wants to use services that run under another web context like Monitoring.

We strongly distinguish `Authorization and Authentication <https://www.okta.com/identity-101/authentication-vs-authorization/>`_.

*Authentication* is the process of ensuring a User is who he claims to be (by checking his password).
This step is delegated to the OAuth2 provider.

*Authorization* means to provide each User the proper rights to do only the actions he or she is allowed to do and only see the appropriate data.
As an example consider the creation of a new Asset which should normally only be done by users with elevated rights.
The whole authorization process is done in Django and based on the OMAP data model.

Asset Management
----------------

Besides users and user management another core functionality of the platform is the management of assets.
Assets can be all kind of things, not just machines.
Other examples are robots or other inventory used together in a production context.

*Assets* use `UUID <https://de.wikipedia.org/wiki/Universally_Unique_Identifier>`_ s as primary keys so they can be shared easily between separate instances.
As *assets* are at the heart of the OMAP they contain a many properties that are used throught many apps.
There is even to possibility to share an asset between separate :ref:`Organizations<Customer Management>` where each organization has another role, e.g. one is the producer, one is the owner and so on.

Customer Management
-------------------

The third crucial component of the OMAP is the management of customers. In many situations emploees of the customers are also users (thats what the platform is for!).


.. include:: e2e.rst
