from __future__ import annotations

# Standard library imports.
from typing import Sequence, List, Optional

# Project imports.
import disruptive as dt
import disruptive.requests as req
from disruptive.events import Event
from disruptive.authentication import BasicAuth, OAuth


class EventHistory():

    @staticmethod
    def get(project_id: str,
            device_id: str,
            event_types: Optional[Sequence[str]] = None,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None,
            auth: Optional[BasicAuth | OAuth] = None,
            ) -> List[Event]:

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['eventTypes'] = event_types
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
            params['endTime'] = end_time

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)

        # Send paginated GET request.
        res = req.auto_paginated_list(
            url=url,
            pagination_key='events',
            params=params,
            page_size=1000,
            auth=auth,
        )

        # Return list of Event objects of paginated GET response.
        return Event.from_mixed_list(res)
