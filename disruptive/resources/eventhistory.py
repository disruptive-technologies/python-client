from __future__ import annotations

from typing import Optional, Any
from datetime import datetime

import disruptive.requests as dtrequests
import disruptive.transforms as dttrans
from disruptive.events.events import Event


class EventHistory():
    """
    Contains staticmethods for streaming events.
    Used for namespacing only and thus does not have a constructor

    """

    @staticmethod
    def list_events(device_id: str,
                    project_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str | datetime] = None,
                    end_time: Optional[str | datetime] = None,
                    **kwargs: Any,
                    ) -> list[Event]:
        """
        Get the event history for a single device.

        Parameters
        ----------
        device_id : str
            Unique ID of the target device.
        project_id : str
            Unique ID of the target project.
        event_types : list[str], optional
            If provided, only the specified
            :ref:`event types <event_types>` are fetched.
        start_time : str, datetime, optional
            Specifies from when event history is fetched.
            Defaults to 24 hours ago.
        end_time : str, datetime, optional
            Specified until when event history is fetched.
            Defaults to now.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        events : list[Event]
            A list of all events fetched by the call.

        Examples
        --------
        >>> # Fetch all historic events the last 24 hours.
        >>> events = disruptive.EventHistory.list_events(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID',
        ... )

        >>> # Create a datetime object for 7 days ago.
        >>> from datetime import datetime, timedelta
        >>> seven_days_ago = datetime.now() - timedelta(7)
        >>>
        >>> # Fetch objectPresent event history the last 7 days.
        ... events = dt.EventHistory.list_events(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID>',
        ...     event_types=['objectPresent'],
        ...     start_time=seven_days_ago,
        ... )

        """

        # Construct URL.
        url = '/projects/{}/devices/{}/events'.format(project_id, device_id)

        # Construct parameters dictionary.
        params: dict = dict()
        if event_types is not None:
            params['eventTypes'] = event_types

        # Sanitize timestamps as they must be iso8601 format.
        start_time_iso8601 = dttrans.to_iso8601(start_time)
        if start_time_iso8601 is not None:
            params['startTime'] = start_time_iso8601
        end_time_iso8601 = dttrans.to_iso8601(end_time)
        if end_time_iso8601 is not None:
            params['endTime'] = end_time_iso8601

        # Send paginated GET request.
        res = dtrequests.DTRequest.paginated_get(
            url=url,
            pagination_key='events',
            params=params,
            **kwargs,
        )

        # Return list of Event objects of paginated GET response.
        events: list[Event] = Event.from_mixed_list(res)
        return events
