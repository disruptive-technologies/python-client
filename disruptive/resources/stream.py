from __future__ import annotations

# Standard library imports
from typing import Sequence, Generator, Optional

# Project Imports.
import disruptive as dt
from disruptive.events import Event
from disruptive.authentication import BasicAuth, OAuth


class Stream():

    @staticmethod
    def single(project_id: str,
               device_id: str,
               event_types: Optional[Sequence[str]] = None,
               auth: Optional[BasicAuth | OAuth] = None,
               ) -> Generator:

        # Construct parameters dictionary.
        params: dict = dict()
        params['ping_interval'] = '{}s'.format(dt.ping_interval)
        if event_types is not None:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices/{}:stream'.format(project_id, device_id)
        for event in dt.requests.stream(url, params):
            yield Event(event)

    @staticmethod
    def project(project_id,
                device_ids: Optional[Sequence[str]] = None,
                label_filters: Optional[Sequence[str]] = None,
                device_types: Optional[Sequence[str]] = None,
                event_types: Optional[Sequence[str]] = None,
                auth: Optional[BasicAuth | OAuth] = None,
                ):

        # Construct parameters dictionary.
        params: dict = dict()
        params['ping_interval'] = '{}s'.format(dt.ping_interval)
        if device_ids is not None:
            params['device_ids'] = device_ids
        if device_types is not None:
            params['device_types'] = device_types
        if label_filters is not None:
            params['label_filters'] = label_filters
        if event_types is not None:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices:stream'.format(project_id)
        for event in dt.requests.stream(url, params):
            yield Event(event)
