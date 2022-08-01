from __future__ import annotations

from typing import Optional, Any
from datetime import datetime

import disruptive
import disruptive.requests as dtrequests
import disruptive.transforms as dttrans
from disruptive.events.events import Event


class EventHistory(list):
    """
    Namespacing type of event history methods.
    Inherits list, with some extra functionality.

    """

    @staticmethod
    def list_events(device_id: str,
                    project_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str | datetime] = None,
                    end_time: Optional[str | datetime] = None,
                    **kwargs: Any,
                    ) -> EventHistory:
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
        events : EventHistory[Event]
            A list of all events fetched by the call.

        Examples
        --------
        >>> # Fetch all events in the last 24h for a device.
        >>> events = dt.EventHistory.list_events(
        ...     device_id='<DEVICE_ID>',
        ...     project_id='<PROJECT_ID',
        ... )

        >>> # Fetch all touch- and objectPresent events
        >>> # for a device in the last 7 days.
        >>> events = dt.EventHistory.list_events(
        ...     device_id=DEVICE_1,
        ...     project_id=PROJECT_ID,
        ...     event_types=[
        ...         dt.events.TOUCH,
        ...         dt.events.OBJECT_PRESENT,
        ...     ],
        ...     start_time=datetime.utcnow() - timedelta(7),
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
        return EventHistory(Event.from_mixed_list(res))

    def to_dataframe(self) -> Any:
        """
        Experimental function to convert a list of events to DataFrame.
        Requires the installation of additional packages.
        >> pip install disruptive[extra]

        The `pandas` package is not, and will not, be a dependency of
        the core `disruptive` package. However, supporting DataFrames is a
        significant enough convenience that we're experimenting with it here.
        May be removed in the future if we decide that this is not a good idea.

        The columns `device_id`, `event_id`, and `event_type` are static, then
        one additional column is concatenated for every eventData field.

        Returns
        -------
        df : pandas.DataFrame
            DataFrame of all events in response.

        Raises
        ------
        ModueNotFoundError
            If we pandas package is not installed.

        """

        try:
            import pandas  # type: ignore
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                'Missing package `pandas`.\n\n'
                'to_dataframe() requires additional third-party packages.\n'
                '>> pip install disruptive[extra]'
            )

        rows = []
        for event in self:
            base = {
                'device_id': event.device_id,
                'event_id': event.event_id,
                'event_type': event.event_type,
            }

            if event.event_type == disruptive.events.TEMPERATURE:
                rows += [{
                        **base,
                        **sample.raw,
                    } for sample in event.data.samples
                ]
            else:
                rows.append({**base, **event.data.raw})

        df = pandas.json_normalize(
            rows, None, ['device_id', 'event_id', 'event_type'],
            errors='ignore',
        )

        # Convert columns headers from camelCase to snake_case for consistency.
        map = {name: dttrans.camel_to_snake_case(name) for name in df.columns}
        df = df.rename(columns=map)

        return df
