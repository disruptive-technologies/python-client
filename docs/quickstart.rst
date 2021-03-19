
Quickstart
==========
This is how to get started.

Authenticating the REST API
---------------------------
This can be done in 1, 2, 3.

.. code-block:: python

   # Import the disruptive package.
   import disruptive as dt

   # Set global authentication object.
   dt.auth = BasicAuth(key_id, secret, email)  # BasicAuth
   dt.auth = OAuth(key_id, secret, email)      # OAuth

See? Simple.
