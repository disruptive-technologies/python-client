import disruptive as dt
import disruptive.requests as req

from disruptive.events import Event


class EventHistory():

    def __init__(self, event_list):
        # Initialise variables.
        self.events = Event.from_mixed_list(event_list)

    @classmethod
    def device(cls,
               project_id,
               device_id,
               event_types=[],
               start_time=None,
               end_time=None,
               auth=None,
               ):
        # Construct parameters dictionary.
        params = {}
        if len(event_types) > 0:
            params['eventTypes'] = event_types
        if start_time is not None:
            params['startTime'] = start_time
        if end_time is not None:
            params['endTime'] = end_time

        url = dt.base_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)
        res = req.auto_paginated_list(
            url=url,
            pagination_key='events',
            params=params,
            auth=auth,
        )
        return cls(res)

    @property
    def temperature(self):
        return [e.value for e in self.events if e.type == 'temperature']

    def get_temperature(self):
        t = [e.timestamp for e in self.events if e.type == 'temperature']
        v = [e.value for e in self.events if e.type == 'temperature']
        return t, v
