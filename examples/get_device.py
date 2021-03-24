# Standard library imports.
import os

# Import disruptive package.
import disruptive as dt

# Authenticate the package using serviceaccount credentials.
dt.auth = dt.Auth.serviceaccount(
    key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
    secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
    email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
)

# Get the device of interest.
device = dt.Device.get_device(
    project_id=os.environ.get('DT_PROJECT_ID', ''),
    device_id=os.environ.get('DT_DEVICE_ID', ''),
)

# Print the device information to console.
print(device)
