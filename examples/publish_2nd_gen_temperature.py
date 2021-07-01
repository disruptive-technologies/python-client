import os
from datetime import datetime, timedelta
import disruptive as dt

# Fetch credentials and device info from environment.
key_id = os.getenv('DT_SERVICE_ACCOUNT_KEY_ID')
secret = os.getenv('DT_SERVICE_ACCOUNT_SECRET')
email = os.getenv('DT_SERVICE_ACCOUNT_EMAIL')
device_id = os.getenv('DT_DEVICE_ID')

# Authenticate the package using Service Account credentials.
dt.default_auth = dt.Auth.service_account(key_id, secret, email)

# Create initial values of temperature and time.
timestamp_now = datetime.utcnow()
temperature_now = 22.3

# Generate a list of 5 temperature samples, spread evenly in time.
samples = []
n_samples = 5
for i in range(n_samples):
    samples.append(dt.events.TemperatureSample(
        celsius=temperature_now-i,
        timestamp=timestamp_now-timedelta(seconds=int(i*((15*60)/n_samples))),
    ))

# Publish an emulated temperature event with inter-heartbeat samples.
dt.Emulator.publish_event(
    device_id=os.getenv('DT_DEVICE_ID'),
    project_id=os.getenv('DT_PROJECT_ID'),
    data=dt.events.Temperature(
        celsius=temperature_now,
        timestamp=timestamp_now,
        samples=samples,
    )
)
