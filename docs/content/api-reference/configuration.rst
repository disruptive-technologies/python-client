Configuration
=============
While this package does not require any configuration from the user, certain variables have been explicitly exposed and can be changed to alter different behaviors should one be inclined.

Package-Wide
------------
The following snippet shows the various variables that can be configured and their default values. Setting a new value directly on the package itself, as shown below, will alter the behavior for all methods in the package at once.

.. code-block:: python

   # Import the disruptive package.
   import disruptive as dt

   # If True, information about outgoing requests is printed.
   dt.log = False

   # Number of seconds to wait for a response before giving up.
   request_timeout = 3

   # Number of times to retry a request if an error is returned.
   request_retries = 3

   # Base API URL from which all endpoints are expanded.
   api_url = 'https://api.d21s.com/v2'

   # Same as the previous, but for the emulator API.
   emulator_url = 'https://emulator.d21s.com/v2'

   # Full URL to which token exchange request is sent.
   auth_url = 'https://identity.d21s.com/oauth2/token'

Per-Request
-----------
Each API method in the package can also be configured individually with the aforementioned variables. This will not update the package-wide behavior, only affecting the one call.

.. code-block:: python

   # Fetch all temperature sensors in a project.
   sensors = dt.Device.list_devices(
       project_id,
       # The following configurations are specific for this call.
       log=False,
       api_url='https://api.d21s.com/v2/',
       request_retries=3,
       request_timeout=3,
   )
