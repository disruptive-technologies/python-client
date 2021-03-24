import os
import disruptive as dt

dt.Auth.serviceaccount(
    key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID', ''),
    secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET', ''),
    email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL', ''),
)

device = dt.Device.get_device(
    project_id=os.environ.get('DT_PROJECT_ID', ''),
    device_id=os.environ.get('DT_DEVICE_ID', ''),
)

print(device.id)
