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
