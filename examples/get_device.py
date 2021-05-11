import os

import disruptive as dt

# Fetch credentials and device info from environment.
key_id = os.getenv('DT_SERVICE_ACCOUNT_KEY_ID', '')
secret = os.getenv('DT_SERVICE_ACCOUNT_SECRET', '')
email = os.getenv('DT_SERVICE_ACCOUNT_EMAIL', '')
device_id = os.getenv('DT_DEVICE_ID', '')

# Authenticate the package using Service Account credentials.
dt.default_auth = dt.Auth.service_account(key_id, secret, email)

# Get the device of interest.
device = dt.Device.get_device(device_id)

# Print the device information to console.
print(device)
