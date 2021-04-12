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
        device_id=sensor.id,
        event_types=[dt.EventTypes.temperature],
        start_time=datetime.today()-timedelta(days=7),
    )

    # Print how many events were fetched.
    print('{}: {} events fetched.'.format(
        sensor.id, len(history.events_list)
    ))

    # Isolate timeaxis and temperature data which can be plotted directly.
    timeaxis, temperature = history.get_data_axes('timestamp', 'temperature')
