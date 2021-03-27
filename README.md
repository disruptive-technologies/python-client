# Disruptive Python

![build](https://github.com/disruptive-technologies/disruptive-python/actions/workflows/build.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.7%2C%203.8%2C%203.9-blue)
![coverage](https://img.shields.io/badge/coverage-77%25-green)

## Documentation

TBA

## Installation

The package can be installed through pip:

```sh
pip install disruptive
```

or from source:

```sh
python setup.py install
```

### Requirements

- Python 3.7+

## Usage

Authenticate the library using [Service Account](https://developer.disruptive-technologies.com/docs/service-accounts/creating-a-service-account) credentials by setting `dt.auth`:

```python
import disruptive as dt
dt.auth = dt.Auth.serviceaccount(key_id, secret, email)
```

Provided the account has sufficient [access rights](https://developer.disruptive-technologies.com/docs/service-accounts/managing-access-rights), the various resource methods can now be utilized.

The following example fetched a single temperature sensor, prints it, then checks its historic values.

```python
# Fetch the temperature event history (defaults to 24h ago to now).
temp_events = dt.EventHistory.list_events(
    project_id=temp_sensor.project_id,
    device_id=temp_sensor.id,
    event_types=['temperature'],
)

# Check if any of the event values exceeded 45 degrees Celsius.
if max([e.data.temperature for e in temp_events]):
    print('Too hot!')
```

This second example fetches a list of all touch- and proximity sensors in a project, then sets a new label for all of them.

```python
# Fetch all touch- and proximity sensors in a project.
devices = dt.Device.list(
    project_id='...',
    device_types=[
        'touch',
        'proximity',
    ]
)

# Set a new label for each device in the list.
dt.Device.batch_update_labels(
    project_id='...',
    device_ids=[device.id for device in devices],
    set_labels={'room-number': '99'},
)
```

Finally, the following snippet shows how to stream temperature events sensors in a project.

```python
# Wait for new events to be yielded by the generator.
for e in dt.Stream.project(project_id, event_types=['temperature']):
    # Print event data as they arrive.
    print(e.data)
```

