import os
from datetime import datetime, timedelta

import disruptive as dt

# Fetch credentials and device info from environment.
key_id = os.getenv("DT_SERVICE_ACCOUNT_KEY_ID")
secret = os.getenv("DT_SERVICE_ACCOUNT_SECRET")
email = os.getenv("DT_SERVICE_ACCOUNT_EMAIL")
device_id = os.getenv("DT_DEVICE_ID")

# Authenticate the package using Service Account credentials.
dt.default_auth = dt.Auth.service_account(key_id, secret, email)

# Fetch a list of all temperature event within the last 7 days.
events = dt.EventHistory.list_events(
    device_id=os.getenv("DT_DEVICE_ID"),
    project_id=os.getenv("DT_PROJECT_ID"),
    event_types=[dt.events.TEMPERATURE],
    start_time=datetime.utcnow() - timedelta(days=7),
)

# Create lists into which we will group all samples.
timestamps = []
values = []

# Iterate through list of fetched events.
for event in events:
    # Concatenate samples list to the total group.
    timestamps += [sample.timestamp for sample in event.data.samples]
    values += [sample.celsius for sample in event.data.samples]

# Plot the output. This requires matplotlib to be installed.
# import matplotlib.pyplot as plt
# plt.plot(timestamps, values, '.-')
# plt.show()
