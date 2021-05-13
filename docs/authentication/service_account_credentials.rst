.. _service_account_auth:

Service Account
===============
Authenticates the API using Service Account credentials. Details about the authentication flow implementation can be found in our `OAuth2 Example <https://developer.disruptive-technologies.com/docs/authentication/oauth2>`_.

Preliminaries
-------------
- To authenticate using this method, a Service Account with sufficient permissions is required. If you're unfamiliar with this concept, read our `Introduction to Service Accounts <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_.

Usage
-----
The following snippet authentications all functionality in the package at once.

.. code-block:: python

   import os
   import disruptive as dt

   # It is good practice to fetch credentials from an environment or file.
   key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   
   # Using the fetched credentials, authenticate the package.
   dt.default_auth = dt.Auth.service_account(key_id, secret, email)

Method
------
.. autofunction:: disruptive.Auth.service_account

Class
-----
.. autoclass:: disruptive.authentication.ServiceAccountAuth
