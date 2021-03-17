import os
import disruptive as dt

dt.Auth.oauth(
    key_id=str(os.environ.get('DT_SERVICE_ACCOUNT_KEY_ID')),
    secret=str(os.environ.get('DT_SERVICE_ACCOUNT_SECRET')),
    email=str(os.environ.get('DT_SERVICE_ACCOUNT_EMAIL')),
)

device = dt.Device.get(
    project_id=str(os.environ.get('DT_PROJECT_ID')),
    device_id=str(os.environ.get('DT_DEVICE_ID')),
)

print(device.id)
