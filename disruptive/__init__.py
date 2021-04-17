# Metadata
__version__ = "0.2.1"

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
default_auth = Auth({})

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

# Additional helper modules.
import disruptive.types as types  # noqa
import disruptive.events as events  # noqa
import disruptive.dataconnector_configs as dataconnector_configs  # noqa

# If True, debug information is sent to stdout.
log = False

# REST API base URLs of which all endpoints are an expansion.
api_url = 'https://api.disruptive-technologies.com/v2'
emulator_url = 'https://emulator.disruptive-technologies.com/v2'
auth_url = 'https://identity.disruptive-technologies.com/oauth2/token'

# If a request response contains an error for which a series of retries is
# worth considering, these variable determine how long to wait without an
# answer, and how many times the package should retry before raising an error.
request_timeout = 3  # seconds
request_retries = 3  # attempts
