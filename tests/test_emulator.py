import sys
from typing import Optional
from dataclasses import dataclass
import datetime

import pytest

import disruptive as dt
import tests.api_responses as dtapiresponses


class TestEmulator():

    def test_create_device(self, request_mock):
        # Update the response data with device data.
        res = dtapiresponses.created_temperature_emulator
        request_mock.json = res

        # Call Emulator.create_device() method.
        d = dt.Emulator.create_device(
            project_id='project_id',
            device_type='temperature',
            display_name='new-device',
            labels={'key': 'value'},
        )

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='POST',
            url=dt.emulator_base_url+'/projects/project_id/devices',
            body={
                'type': 'temperature',
                'labels': {
                    'key': 'value',
                    'name': 'new-device',
                },
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instance of Device object.
        assert isinstance(d, dt.Device)

    def test_delete_device(self, request_mock):
        # Call Emulator.delete_device() method.
        d = dt.Emulator.delete_device(
            device_id='device_id',
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.emulator_base_url+'/projects/project_id/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert d is None

    def test_publish_event(self, request_mock):
        project_id = 'test_project'
        device_id = 'test_device'
        url = dt.emulator_base_url
        url += f'/projects/{project_id}/devices/{device_id}:publish'
        args = {'device_id': device_id, 'project_id': project_id}

        # datetime.datetime.utcnow() is deprecated in Python 3.12
        if sys.version_info.major >= 3 and sys.version_info.minor >= 11:
            now = datetime.datetime.now(datetime.UTC)
        else:
            now = datetime.datetime.utcnow()

        @dataclass
        class TestCase:
            name: str
            give_type: str
            give_data: object
            want_err: Optional[Exception]

        tests = [
            TestCase(
                name='touch',
                give_type=dt.events.TOUCH,
                give_data=dt.events.Touch(now),
                want_err=None,
            ),
            TestCase(
                name='temperature w/o samples',
                give_type=dt.events.TEMPERATURE,
                give_data=dt.events.Temperature(
                    timestamp=now,
                    celsius=23.0,
                ),
                want_err=None,
            ),
            TestCase(
                name='temperature w/ samples',
                give_type=dt.events.TEMPERATURE,
                give_data=dt.events.Temperature(
                    timestamp=now,
                    celsius=23.0,
                    samples=[
                        dt.events.TemperatureSample(23.1, now),
                        dt.events.TemperatureSample(23.2, now),
                        dt.events.TemperatureSample(23.3, now),
                        dt.events.TemperatureSample(23.4, now),
                        dt.events.TemperatureSample(23.5, now),
                    ],
                ),
                want_err=None,
            ),
            TestCase(
                name='object present',
                give_type=dt.events.OBJECT_PRESENT,
                give_data=dt.events.ObjectPresent(
                    timestamp=now,
                    state='PRESENT',
                ),
                want_err=None,
            ),
            TestCase(
                name='humidity',
                give_type=dt.events.HUMIDITY,
                give_data=dt.events.Humidity(
                    timestamp=now,
                    celsius=23.2,
                    relative_humidity=77.7,
                ),
                want_err=None,
            ),
            TestCase(
                name='object present count',
                give_type=dt.events.OBJECT_PRESENT_COUNT,
                give_data=dt.events.ObjectPresentCount(
                    timestamp=now,
                    total=2338,
                ),
                want_err=None,
            ),
            TestCase(
                name='touch count',
                give_type=dt.events.TOUCH_COUNT,
                give_data=dt.events.TouchCount(
                    timestamp=now,
                    total=2338,
                ),
                want_err=None,
            ),
            TestCase(
                name='water present',
                give_type=dt.events.WATER_PRESENT,
                give_data=dt.events.WaterPresent(
                    timestamp=now,
                    state='PRESENT',
                ),
                want_err=None,
            ),
            TestCase(
                name='network status',
                give_type=dt.events.NETWORK_STATUS,
                give_data=dt.events.NetworkStatus(
                    timestamp=now,
                    signal_strength=98,
                    rssi=-66,
                    transmission_mode='LOW_POWER_STANDARD_MODE',
                    cloud_connectors=[
                        dt.events.NetworkStatusCloudConnector(
                            device_id='ccon 1',
                            signal_strength=99,
                            rssi=-77,
                        ),
                        dt.events.NetworkStatusCloudConnector(
                            device_id='ccon 2',
                            signal_strength=88,
                            rssi=-61,
                        ),
                    ],
                ),
                want_err=None,
            ),
            TestCase(
                name='battery status',
                give_type=dt.events.BATTERY_STATUS,
                give_data=dt.events.BatteryStatus(
                    timestamp=now,
                    percentage=78,
                ),
                want_err=None,
            ),
            TestCase(
                name='labels changed',
                give_type=dt.events.LABELS_CHANGED,
                give_data=dt.events.LabelsChanged(
                    timestamp=now,
                    added={'a': 1},
                    modified={'b': 2},
                    removed=['c'],
                ),
                want_err=None,
            ),
            TestCase(
                name='connection status',
                give_type=dt.events.CONNECTION_STATUS,
                give_data=dt.events.ConnectionStatus(
                    timestamp=now,
                    connection='ETHERNET',
                    available=['ETHERNET', 'CELLULAR'],
                ),
                want_err=None,
            ),
            TestCase(
                name='ethernet status',
                give_type=dt.events.ETHERNET_STATUS,
                give_data=dt.events.EthernetStatus(
                    timestamp=now,
                    mac_address='abc',
                    ip_address='123',
                ),
                want_err=None,
            ),
            TestCase(
                name='cellular status',
                give_type=dt.events.CELLULAR_STATUS,
                give_data=dt.events.CellularStatus(
                    timestamp=now,
                    signal_strength=87,
                ),
                want_err=None,
            ),
            TestCase(
                name='co2',
                give_type=dt.events.CO2,
                give_data=dt.events.Co2(
                    timestamp=now,
                    ppm=2000,
                ),
                want_err=None,
            ),
            TestCase(
                name='pressure',
                give_type=dt.events.PRESSURE,
                give_data=dt.events.Pressure(
                    timestamp=now,
                    pascal=899,
                ),
                want_err=None,
            ),
            TestCase(
                name='motion',
                give_type=dt.events.MOTION,
                give_data=dt.events.Motion(
                    timestamp=now,
                    state='NO_MOTION_DETECTED',
                ),
                want_err=None,
            ),
            TestCase(
                name='contact',
                give_type=dt.events.CONTACT,
                give_data=dt.events.Contact(
                    timestamp=now,
                    state='OPEN',
                ),
                want_err=None,
            ),
            TestCase(
                name='probeWireStatus',
                give_type=dt.events.PROBE_WIRE_STATUS,
                give_data=dt.events.ProbeWireStatus(
                    timestamp=now,
                    state='THREE_WIRE',
                ),
                want_err=None,
            ),
        ]

        i = 0
        for test in tests:
            args['data'] = test.give_data

            if test.want_err is None:
                dt.Emulator.publish_event(**args)

                request_mock.assert_requested(
                    method='POST',
                    url=url,
                    body={test.give_type: test.give_data._raw},
                )

                request_mock.assert_request_count(i + 1)
                i += 1
            else:
                with pytest.raises(test.want_err):
                    dt.Emulator.publish_event(**args)
