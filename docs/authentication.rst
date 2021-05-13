.. _Authentication:

Authentication
==============
Most of the functionality provided with this Python API requires authenticating with the REST API. Fortunately, provided you are in possession of valid credentials with sufficient `access rights <https://developer.disruptive-technologies.com/docs/service-accounts/managing-access-rights>`_, this can be achieved in a single line of code.

Methods
-------
The following authentication methods are currently available.

.. _authmethods:

- :ref:`Service Account Credentials <service_account_auth>`

Package-Wide
------------

By setting :code:`disruptive.default_auth`, all functionality in the package is authenticated at once.

.. code-block:: python

   import disruptive as dt
   
   # Authenticate all resource methods in the package at once.
   dt.default_auth = dt.Auth.<METHOD>('credentials...')

   # Call any Resource Method.
   device = dt.Device.get_device(device_id)

Per-Requests
------------

Each :ref:`Resource Method <resource_methods>` can also be authenticated individually by directly providing an instance of the authentication method of coice.

Note that this will ignore the package-wide conifguration variable :code:`disruptive.default_auth`.

.. code-block:: python

   # Provide the API Method with an authentication object directly.
   device = dt.Device.get_device(device_id, auth=dt.Auth.<METHOD>('credentials...'))

.. toctree::
   :maxdepth: 1
   :hidden:
   
   authentication/service_account_credentials
