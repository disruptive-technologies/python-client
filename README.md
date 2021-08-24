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

dt.default_auth = dt.Auth.service_account(key_id, secret, email)
```

## Usage

Once authenticated, most functionality can be accessed through resource methods on the following format.

```
disruptive.<Resource>.<method>()
```

A few common uses are showcased in the snippet below. See the [Python API Reference](https://developer.disruptive-technologies.com/api/libraries/python/) for full documentation.

```python
import disruptive as dt

# Fetch a sensor, specified by its ID.
sensor = dt.Device.get_device('<DEVICE_ID>')

# Printing the returned object will list all attributes.
print(sensor)

# Set a new label on the sensor.
dt.Device.set_label(sensor.device_id, sensor.project_id, key='nb', value='99')

# Get touch- and temperature event history for the sensor.
history = dt.EventHistory.list_events(
    sensor.device_id,
    sensor.project_id,
    event_types=[
        dt.events.TOUCH,
        dt.events.TEMPERATURE,
    ]
)

# Initiate an event stream for all devices in the sensor's project.
for event in dt.Stream.event_stream(sensor.project_id):
    # Print new events data as they arrive.
    print(event.data)
```

## Logging
The simplest method is enabled by setting `disruptive.log_level` with a string level.
```python
dt.log_level = 'info'
```
If more fine-grained control is desired, the standard library `logging` can also be used.
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
A few [examples](https://developer.disruptive-technologies.com/api/libraries/python/client/examples.html) has been provided. Before running, the required environment variables listed at the start of each example must be set.

```sh
python examples/example_name.py
```

## Exceptions
If a request is unsuccessful or has been provided with invalid parameters, an exception is raised. A list of available exceptions are available in the [API Reference](https://developer.disruptive-technologies.com/api/libraries/python/client/errors.html).

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
