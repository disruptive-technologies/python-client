*************
API-Reference
*************

The examples provided with methods in the following modules assume that the disruptive package has been imported and authenticated globally.

.. code-block:: python

   # Import disruptive package.
   import disruptive as dt

   # Authenticate globally using either OAuth (recommended) ...
   dt.auth = dt.OAuth(key_id, secret, email)

   # ... or BasicAuth
   dt.auth = dt.BasicAuth(key_id, secret)

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   authentication
   resources/resources
