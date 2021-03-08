

from disruptive.authentication import Auth, BasicAuth, OAuth

from disruptive.resources.device import Device
from disruptive.resources.dataconnector import Dataconnector
from disruptive.resources.organization import Organization
from disruptive.resources.project import Project
from disruptive.resources.stream import Stream
from disruptive.resources.event_history import EventHistory

auth = Auth()

log = False

# explain here
ping_interval = 10
ping_jitter = 2

max_connection_retries = 5

base_url = 'https://api.disruptive-technologies.com/v2'
