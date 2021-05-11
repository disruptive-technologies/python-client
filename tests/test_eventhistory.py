import disruptive
from disruptive.events.events import Event
import tests.api_responses as dtapiresponses


class TestEventHistory():

    def test_list_events(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
            event_types=['temperature', 'touch'],
            start_time='1970-01-01T00:00:00Z',
            end_time='1970-01-02T00:00:00Z',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url
        url += '/projects/project_id/devices/device_id/events'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={
                'eventTypes': ['temperature', 'touch'],
                'startTime': '1970-01-01T00:00:00Z',
                'endTime': '1970-01-02T00:00:00Z',
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output types.
        assert isinstance(h, list)
        for e in h:
            assert isinstance(e, Event)
