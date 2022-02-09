# Metadata
__version__ = "1.2.0"

# Authentication scheme.
from disruptive.authentication import Auth  # noqa

# Initialize package with environment variables authentication scheme.
default_auth = Auth._service_account_env_vars()

# Resources.
from disruptive.resources.device import Device  # noqa
from disruptive.resources.data_connector import DataConnector  # noqa
from disruptive.resources.organization import Organization  # noqa
from disruptive.resources.project import Project  # noqa
from disruptive.resources.stream import Stream  # noqa
from disruptive.resources.eventhistory import EventHistory  # noqa
from disruptive.resources.service_account import ServiceAccount  # noqa
from disruptive.resources.role import Role  # noqa
from disruptive.resources.emulator import Emulator  # noqa

# Additional helper modules.
import disruptive.events as events  # noqa

# If set, logs of chosen level and higher are printed to console.
# Available levels are: debug, info, warning, error, critical.
log_level = None

# REST API base URLs of which all endpoints are an expansion.
base_url = 'https://api.disruptive-technologies.com/v2'
emulator_base_url = 'https://emulator.disruptive-technologies.com/v2'

# If a request response contains an error for which a series of retries is
# worth considering, these variable determine how long to wait without an
# answer, and how many times the package should retry before raising an error.
request_timeout = 3  # seconds
request_attempts = 5  # attempts
