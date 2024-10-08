from unittest import mock
from dataclasses import dataclass

import pytest

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

    def test_to_pandas_polars(self, request_mock):
        cols = ['device_id', 'event_id', 'event_type']

        @dataclass
        class TestCase:
            name: str
            pandas_installed: bool
            polars_installed: bool
            give_events: disruptive.EventHistory
            want_cols: list[str]
            want_len: int

        tests = [
            TestCase(
                name='none installed',
                pandas_installed=False,
                polars_installed=False,
                give_events=disruptive.EventHistory([
                    disruptive.events.Event(dtapiresponses.touch_event),
                ]),
                want_cols=cols + ['update_time'],
                want_len=1,
            ),
            TestCase(
                name='pandas installed',
                pandas_installed=True,
                polars_installed=False,
                give_events=disruptive.EventHistory([
                    disruptive.events.Event(dtapiresponses.touch_event),
                ]),
                want_cols=cols + ['update_time'],
                want_len=1,
            ),
            TestCase(
                name='none installed',
                pandas_installed=False,
                polars_installed=False,
                give_events=disruptive.EventHistory([
                    disruptive.events.Event(dtapiresponses.touch_event),
                ]),
                want_cols=cols,
                want_len=0,
            ),
            TestCase(
                name='no events in response',
                pandas_installed=True,
                polars_installed=True,
                give_events=disruptive.EventHistory([
                ]),
                want_cols=[],
                want_len=0,
            ),
            TestCase(
                name='touch events',
                pandas_installed=True,
                polars_installed=True,
                give_events=disruptive.EventHistory([
                    disruptive.events.Event(dtapiresponses.touch_event),
                    disruptive.events.Event(dtapiresponses.touch_event),
                    disruptive.events.Event(dtapiresponses.touch_event),
                ]),
                want_cols=cols + ['update_time'],
                want_len=3,
            ),
            TestCase(
                name='touch + temperature events',
                pandas_installed=True,
                polars_installed=True,
                give_events=disruptive.EventHistory([
                    disruptive.events.Event(dtapiresponses.touch_event),
                    disruptive.events.Event(dtapiresponses.touch_event),
                    disruptive.events.Event(dtapiresponses.temperature_event),
                    disruptive.events.Event(dtapiresponses.temperature_event),
                    disruptive.events.Event(dtapiresponses.touch_event),
                ]),
                want_cols=cols + ['update_time', 'sample_time', 'value'],
                want_len=5,
            ),
        ]

        for test in tests:
            if test.pandas_installed:
                df_pandas = test.give_events.to_pandas()
                assert len(df_pandas) == test.want_len
                assert len(df_pandas.columns) == len(test.want_cols)
                for col in test.want_cols:
                    assert col in df_pandas.columns
            else:
                patch = 'builtins.__import__'
                with mock.patch(patch, side_effect=ModuleNotFoundError):
                    with pytest.raises(ModuleNotFoundError):
                        test.give_events.to_pandas()

            if test.polars_installed:
                df_polars = test.give_events.to_polars()
                assert df_polars.height == test.want_len
                assert len(df_polars.columns) == len(test.want_cols)
                for col in test.want_cols:
                    assert col in df_polars.columns
            else:
                patch = 'builtins.__import__'
                with mock.patch(patch, side_effect=ModuleNotFoundError):
                    with pytest.raises(ModuleNotFoundError):
                        test.give_events.to_polars()
