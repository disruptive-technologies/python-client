
# Authentication scheme.
from disruptive.authentication import Auth  # noqa

# When auth is an instance of Auth set with the default constructor,
# the package is unauthenticated, throwing an Unauthorized error at call.
# To authorize, either overwrite the global variable `auth` or provide
# each individual method with the same auth object.
#
# Available authentication methods:
# auth = disruptive.Auth.serviceaccount(key_id, secret, email)
#
# Initialize package with unauthenticated object.
auth = Auth(
    method='unauthenticated',
    credentials={},
)

# Resources.
from disruptive.resources.device import Device  # noqa
from disruptive.resources.dataconnector import DataConnector  # noqa
from disruptive.resources.organization import Organization  # noqa
from disruptive.resources.project import Project  # noqa
from disruptive.resources.stream import Stream  # noqa
from disruptive.resources.eventhistory import EventHistory  # noqa
from disruptive.resources.serviceaccount import ServiceAccount  # noqa
from disruptive.resources.role import Role  # noqa
from disruptive.resources.emulator import Emulator  # noqa
from disruptive.types import EventTypes  # noqa

# If True, debug information is sent to stdout.
log = False

# REST API base URLs of which all endpoints are an expansion.
api_url = 'https://api.disruptive-technologies.com/v2'
emulator_url = 'https://emulator.disruptive-technologies.com/v2'

# When streaming it is good practice to ping the connection periodically.
# The ping interval is set in the initial request that establishes a TCP
# connection. By including a timeout with some jitter, the connection will
# automatically reconnect if a ping is not heard within the expected range.
request_timeout = 3  # seconds
request_retries = 3  # attempts
