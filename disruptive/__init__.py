# Metadata
__version__ = '1.4.1'

# Authentication scheme.
from disruptive.authentication import Auth as Auth  # noqa

# Initialize package with environment variables authentication scheme.
default_auth = Auth._service_account_env_vars()

# Resources.
from disruptive.resources.device import Device as Device  # noqa
from disruptive.resources.data_connector import DataConnector as DataConnector  # noqa
from disruptive.resources.organization import Organization as Organization  # noqa
from disruptive.resources.project import Project as Project  # noqa
from disruptive.resources.stream import Stream as Stream  # noqa
from disruptive.resources.eventhistory import EventHistory as EventHistory  # noqa
from disruptive.resources.service_account import ServiceAccount as ServiceAccount  # noqa
from disruptive.resources.role import Role as Role  # noqa
from disruptive.resources.emulator import Emulator as Emulator  # noqa

# Additional helper modules.
from disruptive import events as events  # noqa
from disruptive import outputs as outputs  # noqa
from disruptive import errors as errors  # noqa

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
request_attempts = 3  # attempts
