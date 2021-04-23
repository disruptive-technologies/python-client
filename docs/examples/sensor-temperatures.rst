Plot Temperatures
=================

In this example we are going to fetch the 7-day event history for all temperature sensors in a project, then plot the data axes.

Full Example
------------

.. code-block:: python 

   # Standard library imports.
   import os
   from datetime import datetime, timedelta
   
   # Import disruptive package.
   import disruptive as dt
   
   # Authenticate the package using serviceaccount credentials.
   dt.default_auth = dt.Auth.serviceaccount(
       key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
       secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
       email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
   )
   
   # Fetch all temperature sensors in a project.
   temp_sensors = dt.Device.list_devices(
       project_id=os.environ.get('DT_PROJECT_ID', ''),
       device_types=['temperature'],
   )
   
   # Iterate through each temperature sensor in fetched list.
   for sensor in temp_sensors:
       # Fetch temperature events over the last 7 days.
       history = dt.EventHistory.list_events(
           project_id=sensor.project_id,
           device_id=sensor.device_id,
           event_types=[dt.types.events.temperature],
           start_time=datetime.today()-timedelta(days=7),
       )
   
       # Print how many events were fetched.
       print('{}: {} events fetched.'.format(
           sensor.device_id, len(history.events_list)
       ))
   
       # Isolate timeaxis and temperature data which can be plotted directly.
       timeaxis, temperature = history.get_data_axes('timestamp', 'celsius')

Step-By-Step
------------

Environment variables are used for both fetching credentials and project ID. Therefore, in addition to importing the disruptive package, we also import os.

.. code-block:: python

   # Standard library imports.
   import os
   from datetime import datetime, timedelta
   
   # Import disruptive package.
   import disruptive as dt

Using a Service Account's credentials, all endpoints in the package can be authenticated at once by updating the :code:`dt.default_auth` variable with an Auth object.

.. code-block:: python

   # Authenticate the package using serviceaccount credentials.
   dt.default_auth = dt.Auth.serviceaccount(
       key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
       secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
       email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
   )

Once authenticated, all temperature sensors in the project can be fetched.

.. code-block:: python

   # Fetch all temperature sensors in a project.
   temp_sensors = dt.Device.list_devices(
       project_id=os.environ.get('DT_PROJECT_ID', ''),
       device_types=['temperature'],
   )

The 7-day event history can be fetched for each sensor by iterating the list of sensors.

.. code-block:: python

   # Iterate through each temperature sensor in fetched list.
   for sensor in temp_sensors:
       # Fetch temperature events over the last 7 days.
       history = dt.EventHistory.list_events(
           project_id=sensor.project_id,
           device_id=sensor.device_id,
           event_types=[dt.types.events.temperature],
           start_time=datetime.today()-timedelta(days=7),
       )

       # Print how many events were fetched.
       print('{}: {} events fetched.'.format(
           sensor.device_id, len(history.events_list)
       ))

Once fetched, the returned EventHistory object contains a list of all events and their data.

.. code-block:: python

    # Isolate the timestamp- and temperature data axes and superimpose on plot.
    timeaxis, temperature = history.get_data_axes('timestamp', 'celsius')
