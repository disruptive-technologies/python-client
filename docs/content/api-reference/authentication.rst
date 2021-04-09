.. _Authentication:

Authentication
==============

Most of the package functionality requires authentication towards the REST API.

To authenticate the entire package at once, set the global variable :code:`dt.auth` with a :ref:`routine <routines>`:

.. code-block:: python

   # Import the package.
   import disruptive as dt

   # Set package-wide authentication.
   dt.auth = dt.Auth.serviceaccount(key_id, secret, email)

Alternatively, each API method can be individually authenticated:

.. code-block:: python

   # Create an auth object variable.
   auth_obj = dt.Auth.serviceaccount(key_id, secret, email)
   
   # Provide the object directly to the API method.
   device_list = dt.Device.list_devices(project_id, auth=auth_obj)

.. _routines:

Routines
^^^^^^^^
.. autofunction:: disruptive.Auth.serviceaccount

Class
^^^^^
.. autoclass:: disruptive.Auth
