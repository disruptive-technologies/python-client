import os
from datetime import datetime, timedelta

import disruptive as dt

# Fetch credentials and device info from environment.
key_id = os.getenv("DT_SERVICE_ACCOUNT_KEY_ID", "")
secret = os.getenv("DT_SERVICE_ACCOUNT_SECRET", "")
email = os.getenv("DT_SERVICE_ACCOUNT_EMAIL", "")
device_id = os.getenv("DT_DEVICE_ID", "")
project_id = os.getenv("DT_PROJECT_ID", "")

# Authenticate the package using Service Account credentials.
dt.default_auth = dt.Auth.service_account(key_id, secret, email)

# Define the start-time from when events are fetched.
seven_days_ago = datetime.now() - timedelta(7)

# Fetch humidity events from the past 7 days.
events = dt.EventHistory.list_events(
    device_id=device_id,
    project_id=project_id,
    event_types=[dt.events.HUMIDITY],
    start_time=seven_days_ago,
)

# Iterate through the list of fetched events.
for event in events:
    # Isolate a few values contained within the event.
    event_id = event.event_id
    timestamp = event.data.timestamp
    humidity = event.data.humidity

    # Print a formatted string of the isolated information.
    print(f"{humidity}% humidity from event {event_id} at {timestamp}.")
