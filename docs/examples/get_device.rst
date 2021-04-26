Get Device
==========
In this example, a single device is fetched and printed to console.

Example Code
------------

.. code-block:: python 

   import os
   import disruptive as dt
   
   # Fetch the necessary credentials and variables from environment.
   key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   device_id = os.environ.get('DT_DEVICE_ID', '')
   
   # Authenticate the package using serviceaccount credentials.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)
   
   # Get the device of interest.
   device = dt.Device.get_device(device_id)
   
   # Print the device information to console.
   print(device)

Step-By-Step
------------

Environment variables are used for both credentials and the device ID. Therefore, in addition to importing the `disruptive` package, we also import `os`.

.. code-block:: python

   import os
   import disruptive as dt

   # Fetch the necessary credentials and variables from environment.
   key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   device_id = os.environ.get('DT_DEVICE_ID', '')

Using a Service Account's credentials, all endpoints in the package can be authenticated at once by updating the :code:`dt.default_auth` variable with an Auth object.

.. code-block:: python

   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

Once authenticated, calling the :code:`Device.get_device()` resource method will fetch a single device.

.. code-block:: python

   device = dt.Device.get_device(device_id)

Finally, print the device information to the console.

.. code-block:: python

   print(device)

