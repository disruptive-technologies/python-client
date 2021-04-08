from __future__ import annotations

# Standard library imports.
from typing import Optional
from datetime import datetime

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.transforms as dttrans
from disruptive.events import Event


class EventHistory():
    """
    Contains staticmethods for fetching event history.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def list_events(project_id: str,
                    device_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str | datetime] = None,
                    end_time: Optional[str | datetime] = None,
                    **kwargs,
                    ) -> list[Event]:
        """
        Get the event history for a single device.

        Parameters
        ----------
        project_id : str
            Unique ID of the target project.
        device_id : str
            Unique ID of the target device.
        event_types : list[str], optional
            If provided, only the specified event types are fetched.
        start_time : str, datetime, optional
            Specifies from when event history is fetched.
            Defaults to 24 hours ago.
        end_time : str, datetime, optional
            Specified until when event history is fetched.
            Defaults to now.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        page_size: int, optional
            Number of events [1, 1000] to get per request. Defaults to 1000.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        events : list[Event]
            List of objects each representing an event in fetched history.

        """

        # Construct URL.
        url = dt.api_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['eventTypes'] = event_types

        # Sanitize timestamps as they must be iso8601 format.
        start_time_iso8601 = dttrans.to_iso8601(start_time)
        if start_time_iso8601 is not None:
            params['startTime'] = start_time
        end_time_iso8601 = dttrans.to_iso8601(end_time)
        if end_time_iso8601 is not None:
            params['endTime'] = end_time

        # Send paginated GET request.
        res = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='events',
            params=params,
            **kwargs,
        )

        # Return list of Event objects of paginated GET response.
        return Event.from_mixed_list(res)
