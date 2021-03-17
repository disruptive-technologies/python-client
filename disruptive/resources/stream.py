from __future__ import annotations

# Standard library imports
from typing import Sequence, Generator

# Project Imports.
import disruptive as dt
from disruptive.events import Event


class Stream():

    @staticmethod
    def single(project_id: str,
               device_id: str,
               event_types: Sequence[str] = [],
               ) -> Generator:

        # Construct parameters dictionary.
        params: dict = dict()
        params['ping_interval'] = '{}s'.format(dt.ping_interval)
        if len(event_types) > 0:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices/{}:stream'.format(project_id, device_id)
        for event in dt.requests.stream(url, params):
            yield Event(event)

    @staticmethod
    def project(project_id,
                device_ids=[],
                label_filters=[],
                device_types=[],
                event_types=[],
                ):

        # Construct parameters dictionary.
        params = {'ping_interval': '{}s'.format(dt.ping_interval)}
        if len(device_ids) > 0:
            params['device_ids'] = device_ids
        if len(device_types) > 0:
            params['device_types'] = device_types
        if len(label_filters) > 0:
            params['label_filters'] = label_filters
        if len(event_types) > 0:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices:stream'.format(project_id)
        for event in dt.requests.stream(url, params):
            yield Event(event)
