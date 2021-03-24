Get Device
==========

In this example we are going to fetch a single device from a project, using a Service Account for authentication.

Full Example
------------

.. code-block:: python 

   # Standard library imports.
   import os
   
   # Import disruptive package.
   import disruptive as dt
   
   # Authenticate the package using serviceaccount credentials.
   dt.auth = dt.Auth.serviceaccount(
       key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
       secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
       email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
   )
   
   # Get the device of interest.
   device = dt.Device.get_device(
       project_id=os.environ.get('DT_PROJECT_ID', ''),
       device_id=os.environ.get('DT_DEVICE_ID', ''),
   )
   
   # Print the device information to console.
   print(device)

Step-By-Step
------------

Environment variables are used for both credentials and the device- and project ID. Therefore, in addition to importing the disruptive package, we also import os.

.. code-block:: python

   # Standard library imports.
   import os
   
   # Import disruptive package.
   import disruptive as dt

Using a Service Account's credentials, all endpoints in the package can be authenticated at once by updating the :code:`dt.auth` variable with an Auth object.

.. code-block:: python

   # Authenticate the package using serviceaccount credentials.
   dt.auth = dt.Auth.serviceaccount(
       key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
       secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
       email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
   )

Once authenticated, the device can be fetched by calling the appropriate method.

.. code-block:: python

   # Get the device of interest.
   device = dt.Device.get_device(
       project_id=os.environ.get('DT_PROJECT_ID', ''),
       device_id=os.environ.get('DT_DEVICE_ID', ''),
   )

Finally, print the device information to the console.

.. code-block:: python

   # Print the device information to console.
   print(device)

