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
pip install .
```

### Requirements

- Python 3.7+

## Example Usage

Authenticate the library using [Service Account](https://developer.disruptive-technologies.com/docs/service-accounts/creating-a-service-account) credentials by setting `dt.auth`:

```python
import disruptive as dt
dt.auth = dt.Auth.serviceaccount(key_id, secret, email)
```

Provided the account has sufficient [access rights](https://developer.disruptive-technologies.com/docs/service-accounts/managing-access-rights), the various resource methods can now be utilized.

The following example showcases a few available methods.

```python
# Fetch a specified temperature sensor from a project.
sensor = dt.Device.get_device(project_id='...', device_id='...')

# Set a label on the fetched device.
dt.Device.set_label(
    sensor.project_id,
    sensor.device_id,
    key='room-number',
    value='99',
)

# Get historic touch- and temperature events the last 24h.
events = dt.EventHistory.list_events(
    sensor.project_id,
    sensor.id,
    event_types=['touch', 'temperature'],
)

# Set up a real-time event stream for the sensor.
for new_event in dt.Stream.device(sensor.project_id, sensor.id):
    # Print the data in new events as they arrive.
    print(new_event.data)
```

## Authentication Override

While it is most convenient to authenticate the whole package at once, if a method is provided with an Auth object, this will take priority.

```python
import disruptive as dt

# Package-wide authentication.
dt.auth = dt.Auth.serviceaccount(key_id_1, email_1, secret_1)

# Authenticate the call using a different serviceaccount.
members = dt.Project.list_members(
    project_id,
    auth=dt.Auth.serviceaccount(
        key_id_2,
        secret_2,
        email_2,
    ),
)
```

## Development

Set up the development virtualenv environment:
```
make
```

Run unit-tests against the currently active python version:
```
make test
```

Lint the package code using MyPy and flake8:
```
make lint
```

Build the sphinx documentation:
```
make docs
```

Build the package distribution:
```
make build
```
