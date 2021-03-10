import disruptive as dt
import disruptive.requests as req

from disruptive.events import Event


class EventHistory():

    def __init__(self, event_list):
        # Initialise variables.
        self.events = Event.from_mixed_list(event_list)

    @classmethod
    def single(cls,
               project_id,
               device_id,
               event_types=[],
               start_time=None,
               end_time=None,
               page_size=None,
               auth=None,
               ):

        url = dt.base_url
        url += '/projects/{}/devices/{}/events'.format(project_id, device_id)
        res = req.get(
            url=url,
            auth=auth,
        )
        return cls(res['events'])

    @property
    def temperature(self):
        return [e.value for e in self.events if e.type == 'temperature']

    def get_temperature(self):
        t = [e.timestamp for e in self.events if e.type == 'temperature']
        v = [e.value for e in self.events if e.type == 'temperature']
        return t, v
