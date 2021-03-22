from __future__ import annotations

# Standard library imports.
from typing import Optional, Generator

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
from disruptive.events import Event
from disruptive.authentication import BasicAuth, OAuth


class EventHistory():

    @staticmethod
    def list_events(project_id: str,
                    device_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str] = None,
                    end_time: Optional[str] = None,
                    auth: Optional[BasicAuth | OAuth] = None,
                    ) -> list[Event]:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['eventTypes'] = event_types
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
            params['endTime'] = end_time

        # Send paginated GET request.
        res = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='events',
            params=params,
            page_size=1000,
            auth=auth,
        )

        # Return list of Event objects of paginated GET response.
        return Event.from_mixed_list(res)

    @staticmethod
    def generator(project_id: str,
                  device_id: str,
                  page_size: int = 100,
                  event_types: Optional[list[str]] = None,
                  start_time: Optional[str] = None,
                  end_time: Optional[str] = None,
                  auth: Optional[BasicAuth | OAuth] = None,
                  ) -> Generator:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['eventTypes'] = event_types
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
            params['endTime'] = end_time

        # Relay generator output, yielding Device objects of response.
        for devices in dtrequests.generator_list(
                url=url,
                pagination_key='events',
                params=params,
                page_size=page_size,
                auth=auth
                ):
            for device in devices:
                yield Event(device)
