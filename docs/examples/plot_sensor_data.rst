.. _plot_sensor_data_example:

Plot Sensor Data
================
In this example, 7 days of historic temperature events are fetched and plotted for a sensor.

Full Example
------------
The following snippet implements the example. Remember to set the environment variables.

.. code-block:: python

   import os
   from datetime import datetime, timedelta
   
   import matplotlib.pyplot as plt
   import disruptive as dt
   
   # Fetch credentials and device info from environment.
   key_id = os.getenv('DT_SERVICE_ACCOUNT_KEY_ID', '')
   secret = os.getenv('DT_SERVICE_ACCOUNT_SECRET', '')
   email = os.getenv('DT_SERVICE_ACCOUNT_EMAIL', '')
   device_id = os.getenv('DT_DEVICE_ID', '')
   project_id = os.getenv('DT_PROJECT_ID', '')
   
   # Authenticate the package using Service Account credentials.
   dt.default_auth = dt.Auth.service_account(key_id, secret, email)
   
   # Fetch temperature events for the last 7 days.
   event_history = dt.EventHistory.list_events(
       device_id=device_id,
       project_id=project_id,
       event_types=[dt.events.TEMPERATURE],
       start_time=datetime.today()-timedelta(days=7),
   )
   
   # Isolate timeaxis and temperature data which can be plotted directly.
   timestamps = [event.data.timestamp for event in event_history]
   temperature = [event.data.celsius for event in event_history]
   
   # Generate a plot using the fetched timeaxis and temperature values.
   plt.plot(timestamps, temperature, '.-')
   plt.xlabel('Timestamp')
   plt.ylabel('Temperature [C]')
   plt.show()

.. image:: /examples/plot-sensor-data.png

Explanation
-----------
Using `Service Account <https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts>`_ credentials, the entire package can be authenticated at once by setting the :code:`dt.default_auth` variable with an Auth :ref:`authentication method <authmethods>`.

.. code-block:: python

   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

Once authenticated, the temperature event history can be fetched using the :code:`disruptive.EventHistory.list_events()` resource method. Default timerange is the last 24 hours, but here we provide a `start_time` 7 days ago.

.. code-block:: python

   history = dt.EventHistory.list_events(
       device_id=device_id,
       project_id=project_id,
       event_types=[dt.events.TEMPERATURE],
       start_time=datetime.today()-timedelta(days=7),
   )

The returned `event_history` variable is list containing the fetched :ref:`Events <event>`. Various data can be extracted quickly using simple list comprehension.

.. code-block:: python

   timestamps = [event.data.timestamp for event in event_history]
   temperature = [event.data.celsius for event in event_history]

Finally, provided the `matplotlib` package is installed, the data can be plotted.

.. code-block:: python

   plt.plot(timestamps, temperature, '.-')
   plt.xlabel('Timestamp')
   plt.ylabel('Temperature [C]')
   plt.show()
