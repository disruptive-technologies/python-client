.. _quickstart:

**********
Quickstart
**********

Authentication
==============
Most of the provided functionality requires authentication to the API. Using Service Account credentials, the entire package can be authenticated at once.

.. code-block:: python

   import os
   import disruptive as dt

   # Fetch credentials from environment.
   key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
   email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
   
   # Authenticate the package by setting disruptive.default_auth.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

See the :ref:`Authentication` section for more details.

Usage
=====
API methods are grouped under various resource names on the form :code:`disruptive.<Resource>.<method>()`.

.. code-block:: python

   # Fetch a specific temperature sensor from a project.
   sensor = dt.Device.get_device(device_id)
   
   # Print the sensor information, listing all available attributes.
   print(sensor)
   
   # Set a new label on the sensor.
   dt.Device.set_label(
      device_id=sensor.device_id,
      project_id=sensor.project_id,
      key='nb#', value='99'
   )
   
   # Get touch- and temperature event history for the sensor.
   history = dt.EventHistory.list_events(
       sensor.device_id,
       sensor.project_id,
       event_types=['touch', 'temperature']
   )
   
   # Set up a real-time event stream for the sensor.
   for e in dt.Stream.device(sensor.device_id, sensor.project_id):
       # Print the data in new events as they arrive.
       print(e.data)

See the :ref:`Examples` section for more in-depth usage.
