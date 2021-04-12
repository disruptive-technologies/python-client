*************
API-Reference
*************

Examples provided with the various API methods assumes the package has already been authenticated.

.. code-block:: python

   # Import disruptive package.
   import disruptive as dt

   # Authenticate all API methods in package at once.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   authentication
   resources/resources
   events
   exceptions
   configuration
