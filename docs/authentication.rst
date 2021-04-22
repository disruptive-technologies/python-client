.. _Authentication:

Authentication
==============

Using `Service Account <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_ credentials, setting :code:`disruptive.default_auth` authenticates the package:

.. code-block:: python

   import os
   import disruptive as dt

   # Fetch credentials from environment.
   key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   
   # Authenticate the package by setting disruptive.default_auth.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

Alternatively, if an API Method is directly provided with an instance of the :code:`Auth` class, this will be prioritized over :code:`disruptive.default_auth`.

.. code-block:: python

   # Provide the API Method with an authentication object directly.
   dt.Device.get_device(
       device_id,
       auth=dt.Auth.serviceaccount(
           key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
           secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
           email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
       )
   )

.. _routines:

Authentication Methods
^^^^^^^^^^^^^^^^^^^^^^
There is currently one method of authenticating the API.
.. _authmethods:
.. autofunction:: disruptive.Auth.serviceaccount

Class
^^^^^
.. autoclass:: disruptive.Auth
