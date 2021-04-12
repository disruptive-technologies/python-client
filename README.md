# Disruptive Python

![build](https://github.com/disruptive-technologies/disruptive-python/actions/workflows/build.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.7%2C%203.8%2C%203.9-blue)
![coverage](https://img.shields.io/badge/coverage-77%25-green)

## Documentation

- [Package Documentation](https://developer.disruptive-technologies.com/api/libraries/python/)
- [Developer Documentation](https://developer.disruptive-technologies.com/docs/)

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

## Authentication

All methods in the package can be authenticated using Service Account credentials by setting `disruptive.default_auth` with the following method:

```python
import disruptive as dt
dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)
```

# Usage

The following snippet showcases a few available methods.

```python
# Fetch a specified temperature sensor from a project.
sensor = dt.Device.get_device(project_id, device_id)

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
    sensor.device_id,
    event_types=['touch', 'temperature'],
)

# Set up a real-time event stream for the sensor.
for new_event in dt.Stream.device(sensor.project_id, sensor.device_id):
    # Print the data in new events as they arrive.
    print(new_event.data)
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
