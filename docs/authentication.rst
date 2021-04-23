.. _Authentication:

Authentication
==============
Most of the functionality provided with this Python API requires authenticating with the REST API. Using an available :ref:`Authentication Method <authmethods>`, this can be done in two ways.

By setting :code:`disruptive.default_auth`, the entire package is authenticated at once:

.. code-block:: python

   import os
   import disruptive as dt

   # It is good practice to fetch credentials from an environment or file.
   key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   
   # Using the fetched credentials, authenticate the entire package.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

Each method can also be authenticated directly, which then ignores :code:`disruptive.default_auth`.

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

.. _authmethods:

Authentication Methods
----------------------
There is currently one method of authenticating the API.

.. autofunction:: disruptive.Auth.serviceaccount

Class
-----
.. autoclass:: disruptive.Auth
