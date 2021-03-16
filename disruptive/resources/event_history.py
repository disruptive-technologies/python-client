import disruptive as dt
import disruptive.requests as req

from disruptive.events import Event


class EventHistory():

    @staticmethod
    def get(project_id,
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
