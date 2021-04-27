# Standard library imports.
import json
from unittest.mock import patch

# Third-party imports.
import pytest
import requests

# Project imports.
import disruptive
import disruptive.errors as dterrors
import tests.api_responses as dtapiresponses
from disruptive.events import Event


class TestStream():

    def test_device_arguments(self, request_mock):
        # Call stream with customer kwargs.
        for event in disruptive.Stream.device(
            device_id='device_id',
            project_id='project_id',
            event_types=['temperature', 'touch'],
            request_retries=9,
        ):
            pass

        url = disruptive.api_url
        url += '/projects/project_id/devices/device_id:stream'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={
                'event_types': ['temperature', 'touch'],
                'ping_interval': '10s',
            },
            stream=True,
            timeout=12,
        )

    def test_project_arguments(self, request_mock):
        # Call stream with customer kwargs.
        for event in disruptive.Stream.project(
            project_id='project_id',
            device_ids=['id1', 'id2', 'id3'],
            label_filters=['l1', 'l2'],
            device_types=['temperature', 'touch'],
            event_types=['temperature', 'touch'],
            request_retries=9,
        ):
            pass

        url = disruptive.api_url
        url += '/projects/project_id/devices:stream'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={
                'device_ids': ['id1', 'id2', 'id3'],
                'device_types': ['temperature', 'touch'],
                'label_filters': ['l1', 'l2'],
                'event_types': ['temperature', 'touch'],
                'ping_interval': '10s',
            },
            stream=True,
            timeout=12,
        )

    def test_ping(self, request_mock):
        # Set 5 ping responses.
        request_mock.iter_data = [
            dtapiresponses.stream_ping,
            dtapiresponses.stream_ping,
            dtapiresponses.stream_ping,
            dtapiresponses.stream_ping,
            dtapiresponses.stream_ping,
        ]

        # Mock logging function, which should trigger once for each ping.
        with patch('disruptive.logging.log') as log_mock:
            for event in disruptive.Stream.device('device_id', 'project_id'):
                pass

            # Assert logging called with expected message.
            log_mock.assert_called_with('Ping received.')

            # Logging should have been called once per ping, +1 for GET.
            assert log_mock.call_count == 6

    def test_responses(self, request_mock):
        # Set stream responses.
        ping = dtapiresponses.stream_ping
        temp = dtapiresponses.stream_temperature_event
        nstat = dtapiresponses.stream_networkstatus_event
        request_mock.iter_data = [
            ping, temp, nstat, ping, temp,
            nstat, ping, temp, nstat
        ]

        # Convert bytes strings to expected responses.
        expected = [
            Event(json.loads(temp.decode('ascii'))['result']['event']),
            Event(json.loads(nstat.decode('ascii'))['result']['event']),
            Event(json.loads(temp.decode('ascii'))['result']['event']),
            Event(json.loads(nstat.decode('ascii'))['result']['event']),
            Event(json.loads(temp.decode('ascii'))['result']['event']),
            Event(json.loads(nstat.decode('ascii'))['result']['event']),
        ]

        # Start the stream.
        for i, event in enumerate(disruptive.Stream.project('project_id')):
            # Compare stream event to expected events.
            assert event._raw == expected[i]._raw

    def test_retry_logic_readtimeout(self, request_mock):
        def side_effect_override(**kwargs):
            raise requests.exceptions.ReadTimeout

        # Overwrite request_mock to raise an error.
        request_mock.request_patcher.side_effect = side_effect_override

        # Catch ConnectionError caused by exhausted retries.
        with pytest.raises(dterrors.ReadTimeout):
            # Start a stream, which should rause an error causing retries.
            for event in disruptive.Stream.project(
                    project_id='project_id',
                    request_retries=8):
                pass

        # Verify request is attempted the set number of times (+1).
        request_mock.assert_request_count(9)

    def test_retry_logic_connectionerror(self, request_mock):
        def side_effect_override(**kwargs):
            raise requests.exceptions.ConnectionError

        # Overwrite request_mock to raise an error.
        request_mock.request_patcher.side_effect = side_effect_override

        # Catch ConnectionError caused by exhausted retries.
        with pytest.raises(dterrors.ConnectionError):
            # Start a stream, which should rause an error causing retries.
            for event in disruptive.Stream.project(
                    project_id='project_id',
                    request_retries=7):
                pass

        # Verify request is attempted the set number of times (+1).
        request_mock.assert_request_count(8)