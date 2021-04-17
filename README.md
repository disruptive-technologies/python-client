# Disruptive Technologies Python API

![build](https://github.com/disruptive-technologies/disruptive-python/actions/workflows/build.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.7%2C%203.8%2C%203.9-blue)
![coverage](https://img.shields.io/badge/coverage-87%25-green)

## Documentation

- [Python API Reference](https://developer.disruptive-technologies.com/api/libraries/python/)
- [Developer Documentation](https://developer.disruptive-technologies.com/docs/)

## Installation

The package can be installed through pip:

```sh
pip install --upgrade disruptive
```

or from source:

```sh
pip install .
```

### Requirements

- Python 3.7+

## Authentication

Using [Service Account](https://developer.disruptive-technologies.com/docs/service-accounts/introduction-to-service-accounts) credentials, setting `disruptive.default_auth` authenticates the package:

```python
import disruptive as dt
dt.default_auth = dt.Auth.serviceaccount(key_id, secret, email)
```

## Usage

API methods are grouped under various resource names on the form `disruptive.<Resource>.<method>()`.

```python
# Fetch a specific temperature sensor from a project.
sensor = dt.Device.get_device(device_id)

# Print the sensor information, listing all available attributes.
print(sensor)

# Set a new label on the sensor.
dt.Device.set_label(sensor.device_id, sensor.project_id, key='nb#', value='99')

# Get touch- and temperature event history the last 24 hours for the sensor.
history = dt.EventHistory.list_events(
    sensor.device_id,
    sensor.project_id,
    event_types=['touch', 'temperature']
)

# Set up a real-time event stream for the sensor.
for new_event in dt.Stream.device(sensor.device_id, sensor.project_id):
    # Print the data in new events as they arrive.
    print(new_event.data)
```

## Examples
A few examples showcasing various uses for the package has been provided. They do not require additional dependencies and can, provided the package has been installed, run as a normal script:
```sh
python example_name.py
```
or from root using the source code:
```sh
python -m examples.example_name
```

## Exceptions
If a request is unsuccessful or has been provided with invalid parameters, an exception is raised. A list of available exceptions are available in the [API Reference](https://developer.disruptive-technologies.com/api/libraries/python/).

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
