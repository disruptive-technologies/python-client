# Standard library imports.
import os
from datetime import datetime, timedelta

# Third party imports.
import matplotlib.pyplot as plt

# Import disruptive package.
import disruptive as dt

# Authenticate the package using serviceaccount credentials.
dt.auth = dt.Auth.serviceaccount(
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
    events_list = dt.EventHistory.list_events(
        project_id=sensor.project_id,
        device_id=sensor.id,
        event_types=['temperature'],
        start_time=datetime.today()-timedelta(days=7),
    )

    # Each event in the list contains metadata about the event
    # in addition to the sensor data itself. List comprehension can
    # be used to quickly unwrap the information of interest.
    plt.plot(
        [e.data.timestamp for e in events_list],
        [e.data.temperature for e in events_list],
        label=sensor.id,
    )

# Generated the plot.
plt.legend()
plt.show()
