.. _get_device_example:

Get Device
==========
In this example, a single device is fetched and printed to console.

Full Example
------------
The following snippet implements the example. Remember to set the environment variables.

.. code-block:: python

   import os
   
   import disruptive as dt
   
   # Fetch credentials and device info from environment.
   key_id = os.getenv('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.getenv('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.getenv('DT_SERVICE_ACCOUNT_EMAIL', '')
   device_id = os.getenv('DT_DEVICE_ID', '')
   
   # Authenticate the package using Service Account credentials.
   dt.default_auth = dt.Auth.service_account(key_id, secret, email)
   
   # Get the device of interest.
   device = dt.Device.get_device(device_id)
   
   # Print the device information to console.
   print(device)

This will generate an output similar to the snippet below.

.. code-block::

   Device(
       device_id: str = bfui341o5b7g0093am50,
       project_id: str = br793014jplfqcpoj45g,
       device_type: str = temperature,
       labels: dict = {'inertia-model': '0.025'},
       display_name: str = Fridge,
       is_emulated: bool = False,
       ...
   )

Explanation
-----------
Using `Service Account <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_ credentials, the entire package can be authenticated at once by setting the :code:`dt.default_auth` variable with an Auth :ref:`authentication method <authmethods>`.

.. code-block:: python

   dt.default_auth = dt.Auth.service_account(key_id, secret, email)

Once authenticated, a device can be fetched using the :code:`get_device()` resource method.

.. code-block:: python

   device = dt.Device.get_device(device_id)

The returned `device` variable is an instance of the `Device` class. It contains many different attributes describing the device itself. By printing the variable, all attributes are printed at once.

.. code-block:: python

   print(device)
