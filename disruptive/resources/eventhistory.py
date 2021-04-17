from __future__ import annotations

# Standard library imports.
from typing import Optional
from datetime import datetime

# Project imports.
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans
from disruptive.events.events import Event


class EventHistory(dtoutputs.OutputBase):
    """
    Contains staticmethods for fetching event history.
    Used for namespacing only and thus does not have a constructor

    Attributes
    ----------
    events_list : list[Event]
        List of all events fetched in history.

    """

    def __init__(self, events_list: list[Event]) -> None:
        """
        Constructs the EventHistory object from a list of events.

        Parameters
        ----------
        events_list : list[Event]
            A list of event objects, each representing a single event.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, {})

        # Set parameter attributes.
        self.events_list = events_list

    @classmethod
    def list_events(cls,
                    device_id: str,
                    project_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str | datetime] = None,
                    end_time: Optional[str | datetime] = None,
                    **kwargs,
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
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        history : EventHistory
            Object containing each event in history in addition to a few
            convenience functions.

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
        return cls(Event.from_mixed_list(res))

    def get_events(self, event_type):
        """
        Returns a filtered list of events specified by type from history.

        Parameters
        ----------
        event_type : str
            The event type to be returned.

        Returns
        -------
        events : list
            List of event objects of the specified type.

        """

        out = []
        for e in self.events_list:
            if e.event_type == event_type:
                out.append(e)
        return out

    def get_data_axes(self,
                      x_name: str,
                      y_name: Optional[str] = None,
                      event_type: Optional[str] = None,
                      ):
        """
        Returns filtered lists of the data axes as specified from
        event type in history.

        Parameters
        ----------
        x_name : str
            Name of the first axis to isolate.
        y_name : str, optional
            Name of the second axis to isolate.
        event_type : str, optional
            Filter by event type. For instance, "state" exists for both
            waterPresent and objectPresent event types.

        Returns
        -------
        x_axis : list
            List of values on the first axis.
        y_axis : list
            List of values on the second axis.

        """

        x_axis = []
        y_axis = []
        for e in self.events_list:
            # Skip event if event_type mismatch.
            if event_type is not None and event_type != e.event_type:
                continue

            # Skip event if x- or y-name does not exist.
            if not hasattr(e.data, x_name):
                continue
            if y_name is not None and not hasattr(e.data, y_name):
                continue

            # Tests passed, append timestamp and y-axis.
            x_axis.append(getattr(e.data, x_name))
            if y_name is not None:
                y_axis.append(getattr(e.data, y_name))

        if y_name is not None:
            return x_axis, y_axis
        else:
            return x_axis
