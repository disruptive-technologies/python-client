import os
import disruptive as dt

dt.OAuth.authenticate(
    key_id=os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID'),
    secret=os.environ.get('DT_SERVICE_ACCOUNT_SECRET'),
    email=os.environ.get('DT_SERVICE_ACCOUNT_EMAIL'),
)

device = dt.Device.get(
    project_id=os.environ.get('DT_PROJECT_ID'),
    device_id=os.environ.get('DT_DEVICE_ID')
)

print(device.id)
