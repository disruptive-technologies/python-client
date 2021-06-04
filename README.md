# Disruptive Technologies Python Client

![build](https://github.com/disruptive-technologies/python-client/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/gh/disruptive-technologies/python-client/branch/main/graph/badge.svg)](https://codecov.io/gh/disruptive-technologies/python-client)

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

# Using Service Account credentials, authenticate the package.
dt.default_auth = dt.Auth.service_account(key_id, secret, email)
```

## Usage

Assuming you have authenticated correctly, most functionality is accessed through methods grouped under various Resources on the form `disruptive.<Resource>.<method>()`.

```python
import disruptive as dt

# Fetch a specific sensor from a project.
sensor = dt.Device.get_device(device_id)

# Print the sensor information wil list all attributes and values.
print(sensor)

# Set a new label on the sensor.
dt.Device.set_label(sensor.device_id, sensor.project_id, key='nb', value='99')

# Get touch- and temperature event history for the sensor.
history = dt.EventHistory.list_events(
    sensor.device_id,
    sensor.project_id,
    event_types=['touch', 'temperature']
)

# Set up a real-time event stream of all device in project.
for event in dt.Stream.event_stream(sensor.project_id):
    # Print the data in new events as they arrive.
    print(event.data)
```

## Logging
The simplest method is enabled by setting `disruptive.log_level` with a string level.
```python
dt.log_level = 'info'
```
If more fine-grained control is desired, the standard library `logging` module can also be used.
```python
logging.basicConfig(
    filename='example.log',
    format='[%(asctime)s.%(msecs)03d] %(levelname)-8s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.getLogger('disruptive').setLevel(logging.INFO)
``` 
For both methods, the standard levels `debug`, `info`, `warning`, `error`, and `critical` are available.

## Examples
A few [examples](https://developer.disruptive-technologies.com/api/libraries/python/examples/examples.html) has been provided. Before running, the required environment variables listed at the start of each example must be set.

```sh
python examples/example_name.py
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

Build the package distribution:
```
make build
```
