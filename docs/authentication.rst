.. _Authentication:

Authentication
==============
Most of the functionality provided with this Python API requires authenticating with the REST API. Using an available :ref:`Authentication Method <authmethods>`, this can be done in two ways.

By setting :code:`disruptive.default_auth`, the entire package is authenticated at once:

.. code-block:: python

   import disruptive as dt

   # It is good practice to fetch credentials from an environment or file.
   key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   
   # Using the fetched credentials, authenticate the package.
   dt.default_auth = dt.Auth.service_account(key_id, secret, email)

Each method can also be authenticated directly, which then ignores :code:`disruptive.default_auth`.

.. code-block:: python

   # Provide the API Method with an authentication object directly.
   device = dt.Device.get_device(
       device_id='<DEVICE_ID>',
       auth=dt.Auth.service_account(key_id, secret, email)
   )

.. _authmethods:

Authentication Methods
----------------------
There is currently one method of authenticating the API.

.. autofunction:: disruptive.Auth.service_account

Classes
-------
.. autoclass:: disruptive.authentication.ServiceAccountAuth
