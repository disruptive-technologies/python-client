.. _configuration:

Configuration
=============
While this package does not require any configuration from the user, certain variables have been explicitly exposed and can be changed to alter different behaviors should one be inclined.

Package-Wide
------------
The following snippet shows the various variables that can be configured and their default values. Setting a new value directly on the package itself as shown below will alter the behavior for all methods in the package.

.. _config params:

.. code-block:: python

   # Import the disruptive package.
   import disruptive as dt

   # Set to either 'debug', 'info', 'warning', 'error', or 'critical' to enable logging.
   dt.log = None

   # Number of seconds to wait for a response before giving up.
   dt.request_timeout = 3

   # Number of times a request is attempted if an error is returned.
   dt.request_attempts = 3

   # Base API URL from which all endpoints are expanded.
   dt.base_url = 'https://api.d21s.com/v2'

   # Same as the previous, but for the emulator API.
   dt.emulator_base_url = 'https://emulator.d21s.com/v2'

.. _per_request_configuration:

Per-Request
-----------
Each API method in the package can also be configured individually with the aforementioned variables. This will not update the package-wide behavior, only affecting the one call.

.. code-block:: python

   # Fetch all temperature sensors in a project.
   devices = dt.Device.list_devices(
       project_id,
       # The following configurations are specific for this call.
       log=False,
       base_url='https://api.d21s.com/v2',
       request_attempts=3,
       request_timeout=3,
   )
