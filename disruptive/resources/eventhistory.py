from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
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
                    start_time: Optional[str] = None,
                    end_time: Optional[str] = None,
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
        start_time : str, optional
            Specifies from when event history is fetched.
            Defaults to 24 hours ago.
        end_time : str, optional
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
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
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
