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
   dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)
   
   # Fetch temperature events for the last 7 days.
   history = dt.EventHistory.list_events(
       device_id=device_id,
       project_id=project_id,
       event_types=[dt.events.TEMPERATURE],
       start_time=datetime.today()-timedelta(days=7),
   )
   
   # Isolate timeaxis and temperature data which can be plotted directly.
   timeaxis, temperature = history.get_data_axes('timestamp', 'celsius')
   
   # Generate a plot using the fetched timeaxis and temperature values.
   plt.plot(timeaxis, temperature)
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

The returned `history` variable is an instance of the `EventHistory` class. While it contains a list of all fetched events in the :code:`events_list` attribute, we here use the :code:`get_data_axes()` method instead. This returns the event values instead, which is much easier to plot.

.. code-block:: python

   timeaxis, temperature = history.get_data_axes('timestamp', 'celsius')

Finally, provided the `matplotlib` package is installed, the data can be plotted.

.. code-block:: python

   plt.plot(timeaxis, temperature)
   plt.xlabel('Timestamp')
   plt.ylabel('Temperature [C]')
   plt.show()
