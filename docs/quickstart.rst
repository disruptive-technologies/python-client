.. _quickstart:

Quickstart
==========
Our Python 3 API aims to be simple in use without compromising on functionality. Therefore, once authenticated, most tasks can be performed with only a single line of code.

Installation
------------
The package can be installed through pip:

.. code-block:: bash

   pip install --upgrade disruptive

Support is available for Python 3.7+.

Authentication
--------------
Using :ref:`Service Account credentials<service_account_auth>`, setting :code:`disruptive.default_auth` authenticates the package:

.. code-block:: python

   import disruptive as dt
   
   # Using Service Account credentials, authenticate the entire package.
   dt.default_auth = dt.Auth.service_account('<KEY_ID>', '<SECRET>', '<EMAIL>')

You can read about the various ways of authenticating in the :ref:`Authentication` section.

Usage
-----
Assuming you have authenticated correctly, most functionality is accessed through methods grouped under various :ref:`Resources <resource_methods>` on the form :code:`disruptive.<Resource>.<method>()`.

.. code-block:: python

   import disruptive as dt

   # Fetch a specific sensor from a project.
   sensor = dt.Device.get_device(device_id)
   
   # Print the sensor information wil list all attributes and values.
   print(sensor)
   
   # Set a new label on the sensor.
   dt.Device.set_label(sensor.device_id, sensor.project_id, key='nb', value='99')
   
   # Get touch- and temperature event history for the sensor.
   history = dt.EventHistory.list_events(
       sensor.device_id,
       sensor.project_id,
       event_types=['touch', 'temperature']
   )
   
   # Set up a real-time event stream of all device in project.
   for event in dt.Stream.event_stream(sensor.project_id):
       # Print the data in new events as they arrive.
       print(event.data)

See the :ref:`Examples` section for more in-depth usage.
