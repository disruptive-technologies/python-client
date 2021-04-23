.. _quickstart:

**********
Quickstart
**********
Our Python 3 API aims to be simple in use without compromising on functionality. Therefore, once authenticated, most tasks can be performed with only a single line of code.

Authentication
==============
Using `Service Account <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_ credentials, setting :code:`disruptive.default_auth` authenticates the package:

.. code-block:: python

   import os
   import disruptive as dt
   
   # Using Service Account credentials, authenticate the entire package.
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

See the :ref:`Authentication` section for more details.

Usage
=====
Most tasks are performed using methods that are grouped under various resource names on the form :code:`disruptive.<Resource>.<method>()`. Here we show a few quick examples.

.. code-block:: python

   import disruptive as dt

   # Fetch a specific sensor from a project.
   sensor = dt.Device.get_device(device_id)
   
   # Print the sensor information wil list all attributes and values.
   print(sensor)
   
   # Set a new label on the sensor.
   dt.Device.set_label(sensor.device_id, sensor.project_id, key='nb#', value='99')
   
   # Get touch- and temperature event history for the sensor.
   history = dt.EventHistory.list_events(
       sensor.device_id,
       sensor.project_id,
       event_types=['touch', 'temperature']
   )
   
   # Set up a real-time event stream for the sensor.
   for event in dt.Stream.device(sensor.device_id, sensor.project_id):
       # Print the data in new events as they arrive.
       print(event.data)

See the :ref:`Examples` section for more in-depth usage.
