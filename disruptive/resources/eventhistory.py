from __future__ import annotations

# Standard library imports.
from typing import Optional
from datetime import datetime

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans
from disruptive.events import Event


class EventHistory(dtoutputs.OutputBase):
    """
    Contains staticmethods for fetching event history.
    Used for namespacing only and thus does not have a constructor

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
                    project_id: str,
                    device_id: str,
                    event_types: Optional[list[str]] = None,
                    start_time: Optional[str | datetime] = None,
                    end_time: Optional[str | datetime] = None,
                    **kwargs,
                    ) -> EventHistory:
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
            params['startTime'] = start_time_iso8601
        end_time_iso8601 = dttrans.to_iso8601(end_time)
        if end_time_iso8601 is not None:
            params['endTime'] = end_time_iso8601

        # Send paginated GET request.
        res = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='events',
            params=params,
            **kwargs,
        )

        # Return list of Event objects of paginated GET response.
        return cls(Event.from_mixed_list(res))

    def get_touch_events(self):
        """
        Returns a filtered list of touch events from history.

        Returns
        -------
        events : list[Event]
            List of touch events.

        """

        return [e for e in self.events_list if e.event_type == 'touch']

    def get_touch_axes(self):
        """
        Returns filtered list of timestamps from touch events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.

        """

        x = []
        for e in self.events_list:
            if e.event_type == 'touch':
                x.append(e.data.timestamp)
        return x

    def get_temperature_events(self):
        """
        Returns a filtered list of temperature events from history.

        Returns
        -------
        events : list[Event]
            List of temperature events.

        """

        return [e for e in self.events_list if e.event_type == 'temperature']

    def get_temperature_axes(self):
        """
        Returns filtered lists of timestamps and values
        from temperature events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        temperature : list[float]
            List of temperature values in degrees Celsius.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'temperature':
                x.append(e.data.timestamp)
                y.append(e.data.temperature)
        return x, y

    def get_objectpresent_events(self):
        """
        Returns a filtered list of objectPresent events from history.

        Returns
        -------
        events : list[Event]
            List of objectPresent events.

        """

        return [e for e in self.events_list if e.event_type == 'objectPresent']

    def get_objectpresent_axes(self):
        """
        Returns filtered lists of timestamps and state
        from objectPresent events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        state : list[str]
            List of whether an object has been PRESENT or NOT_PRESENT.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'objectPresent':
                x.append(e.data.timestamp)
                y.append(e.data.state)
        return x, y

    def get_humidity_events(self):
        """
        Returns a filtered list of humidity events from history.

        Returns
        -------
        events : list[Event]
            List of humidity events.

        """

        return [e for e in self.events_list if e.event_type == 'humidity']

    def get_humidity_axes(self):
        """
        Returns filtered lists of timestamps, temperature, and humidity values
        from humidity events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        temperature : list[float]
            List of temperature values in degrees Celsius.
        humidity : list[int]
            List of relative humidities in percent.

        """

        x = []
        y = []
        z = []
        for e in self.events_list:
            if e.event_type == 'humidity':
                x.append(e.data.timestamp)
                y.append(e.data.temperature)
                y.append(e.data.humidity)
        return x, y, z

    def get_objectpresentcount_events(self):
        """
        Returns a filtered list of objectPresentCount events from history.

        Returns
        -------
        events : list[Event]
            List of objectPresentCount events.

        """

        return [
            e for e in self.events_list if e.event_type == 'objectPresentCount'
        ]

    def get_objectpresentcount_axes(self):
        """
        Returns filtered lists of timestamps and total counts
        from objectPresentCount events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        total : list[int]
            List of the total number of times the sensor has detected
            the appearance or disappearance of an object over its lifetime.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'objectPresentCount':
                x.append(e.data.timestamp)
                y.append(e.data.total)
        return x, y

    def get_touchcount_events(self):
        """
        Returns a filtered list of touchCount events from history.

        Returns
        -------
        events : list[Event]
            List of touchCount events.

        """

        return [e for e in self.events_list if e.event_type == 'touchCount']

    def get_touchcount_axes(self):
        """
        Returns filtered lists of timestamps and total counts
        from touchCount events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        total : list[int]
            List of the total number of times the sensor
            has been touched over its lifetime.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'touchCount':
                x.append(e.data.timestamp)
                y.append(e.data.total)
        return x, y

    def get_waterpresent_events(self):
        """
        Returns a filtered list of waterPresent events from history.

        Returns
        -------
        events : list[Event]
            List of waterPresent events.

        """

        return [e for e in self.events_list if e.event_type == 'waterPresent']

    def get_waterpresent_axes(self):
        """
        Returns filtered lists of timestamps and states
        from waterPresent events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        state : list[str]
            A list of whether water has been PRESENT or NOT_PRESENT.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'waterPresent':
                x.append(e.data.timestamp)
                y.append(e.data.state)
        return x, y

    def get_networkstatus_events(self):
        """
        Returns a filtered list of networkStatus events from history.

        Returns
        -------
        events : list[Event]
            List of networkStatus events.

        """

        return [e for e in self.events_list if e.event_type == 'networkStatus']

    def get_networkstatus_axes(self):
        """
        Returns filtered lists of timestamps, signal strengths, and rssi
        from networkStatus events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        total : list[int]
            List of the total number of times the sensor has detected
            the appearance or disappearance of an object over its lifetime.

        """

        x = []
        y = []
        z = []
        for e in self.events_list:
            if e.event_type == 'networkStatus':
                x.append(e.data.timestamp)
                y.append(e.data.signal_strength)
                z.append(e.data.rssi)
        return x, y, z

    def get_batterystatus_events(self):
        """
        Returns a filtered list of batteryStatus events from history.

        Returns
        -------
        events : list[Event]
            List of batteryStatus events.

        """

        return [e for e in self.events_list if e.event_type == 'batteryStatus']

    def get_batterystatus_axes(self):
        """
        Returns filtered lists of timestamps and percentages
        from batteryStatus events in history.

        Returns
        -------
        timestamp : list[datetime]
            List of event timestamps.
        percentage : list[int]
            List of coarse percentage estimates (0% to 100%) of
            the remaining battery.

        """

        x = []
        y = []
        for e in self.events_list:
            if e.event_type == 'batteryStatus':
                x.append(e.data.timestamp)
                y.append(e.data.percentage)
        return x, y
