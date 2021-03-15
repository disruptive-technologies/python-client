import disruptive
import disruptive.events as dtevents


class Stream():

    @staticmethod
    def single(project_id,
               device_id,
               event_types=[]
               ):
        # Construct parameters dictionary.
        params = {'ping_interval': '{}s'.format(disruptive.ping_interval)}
        if len(event_types) > 0:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices/{}:stream'.format(project_id, device_id)
        for event in disruptive.requests.stream(url, params):
            yield dtevents.Event(event)

    @staticmethod
    def project(project_id,
                device_ids=[],
                label_filters=[],
                device_types=[],
                event_types=[],
                ):
        # Construct parameters dictionary.
        params = {'ping_interval': '{}s'.format(disruptive.ping_interval)}
        if len(device_ids) > 0:
            params['device_ids'] = device_ids
        if len(device_types) > 0:
            params['device_types'] = device_types
        if len(label_filters) > 0:
            params['label_filters'] = label_filters
        if len(event_types) > 0:
            params['event_types'] = event_types

        # Relay generator output.
        url = '/projects/{}/devices:stream'.format(project_id)
        for event in disruptive.requests.stream(url, params):
            yield dtevents.Event.from_single(event)
