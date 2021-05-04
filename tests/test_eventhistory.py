# Standard library imports.
from datetime import datetime

# Project imports.
import disruptive
from disruptive.events.events import _EVENTS_MAP
import tests.api_responses as dtapiresponses


class TestEventHistory():

    def test_repr(self, request_mock):
        # Update the response data with eventhistory data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Fetch eventhistory for a device.
        x = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Evaluate __repr__ function and compare copy.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_unpack(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Assert attributes in h is in expected form.
        assert isinstance(h, disruptive.EventHistory)
        assert isinstance(h.events_list, list)
        assert len(h.events_list) == len(res['events'])

        # Check that events in history are correct object types.
        for event in h.events_list:
            # event should be instance of Event.
            assert isinstance(event, disruptive.events.Event)

            # Here we determine if the correct event data class in
            # disruptive.events is constructed based on the provided
            # event_type. We do this by using the internal _EVENTS_MAP object
            # to map between the two.
            event_type = event.event_type
            expected = getattr(
                disruptive.events,
                _EVENTS_MAP._api_names[event_type].class_name
            )
            assert isinstance(event.data, expected)

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
        url = disruptive.api_url
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

        # Assert instance of EventHistory object.
        assert isinstance(h, disruptive.EventHistory)

    def test_get_events(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # For each event type, verify get_events only gets that.
        for etype in _EVENTS_MAP._api_names:
            # Fetch events list of specified type.
            events = h.get_events(etype)

            # Iterate events in fetched list and validate type.
            for e in events:
                assert e.event_type == etype

            # Also assert data is instance type.
            exp = getattr(
                disruptive.events,
                _EVENTS_MAP._api_names[etype].class_name
            )
            assert isinstance(e.data, exp)

    def test_get_data_axes(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Fetch timestamps and value for temperature events.
        timestamp, celsius = h.get_data_axes(
            x_name='timestamp',
            y_name='celsius',
        )

        # There is one temperature and one humidity event in res.
        # This should result in 2 celsius entries.
        assert len(timestamp) == 2
        assert len(celsius) == 2

        # Types should also match expected.
        assert isinstance(timestamp, list)
        assert isinstance(celsius, list)
        assert isinstance(timestamp[0], datetime)
        assert isinstance(celsius[0], float)

    def test_get_data_axes_single(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Fetch timestamps and value for temperature events.
        celsius = h.get_data_axes(x_name='celsius')

        # There is one temperature and one humidity event in res.
        # This should result in 2 celsius entries.
        assert len(celsius) == 2

        # Types should also match expected.
        assert isinstance(celsius, list)
        assert isinstance(celsius[0], float)

    def test_get_data_axes_uknown_event_type(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Fetch timestamps and value for temperature events.
        timestamp = h.get_data_axes(x_name='timestamp', event_type='unknown')

        # Nothing should have been found.
        assert isinstance(timestamp, list)
        assert len(timestamp) == 0

    def test_get_data_axes_uknown_axes(self, request_mock):
        # Update the response data with event history data.
        res = dtapiresponses.event_history_each_type
        request_mock.json = res

        # Call EventHistory.list_events() method.
        h = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Fetch timestamps and value for temperature events.
        timestamp, celsius = h.get_data_axes(
            x_name='unknown1',
            y_name='unknown2',
        )

        # Nothing should have been found.
        assert isinstance(timestamp, list)
        assert isinstance(celsius, list)
        assert len(timestamp) == 0
        assert len(celsius) == 0
