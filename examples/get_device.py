import os
import disruptive as dt

# Fetch the necessary credentials and variables from environment.
key_id = os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', '')
secret = os.environ.get('DT_SERVICE_ACCOUNT_SECRET', '')
email = os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', '')
device_id = os.environ.get('DT_DEVICE_ID', '')

# Authenticate the package using serviceaccount credentials.
dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)

# Get the device of interest.
device = dt.Device.get_device(device_id)

# Print the device information to console.
print(device)
