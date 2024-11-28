from datetime import datetime
from dataclasses import dataclass

import disruptive


class TestEvents():

    def test_touch(self):
        x = disruptive.events.Touch(
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_temperature(self):
        x = disruptive.events.Temperature(
            celsius=23,
            is_backfilled=False,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_object_present(self):
        x = disruptive.events.ObjectPresent(
            state='PRESENT',
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_humidity(self):
        now = datetime.now()

        testcases = [
            disruptive.events.Humidity(
                celsius=23,
                relative_humidity=50,
                timestamp=now,
            ),
            disruptive.events.Humidity(
                celsius=23,
                relative_humidity=50,
                samples=[
                    disruptive.events.HumiditySample(
                        celsius=23,
                        relative_humidity=50,
                        timestamp=now,
                    ),
                ],
                timestamp=now,
            ),
        ]

        for t in testcases:
            x = disruptive.events.Humidity(
                celsius=t.celsius,
                relative_humidity=t.relative_humidity,
                timestamp=t.timestamp,
            )
            y = eval(repr(x))
            print(x.raw)
            print(y.raw)
            assert x._raw == y._raw

    def test_object_present_count(self):
        x = disruptive.events.ObjectPresentCount(
            total=9791,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_touch_count(self):
        x = disruptive.events.TouchCount(
            total=183,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_water_present(self):
        x = disruptive.events.WaterPresent(
            state='NOT_PRESENT',
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_network_status(self):
        x = disruptive.events.NetworkStatus(
            signal_strength=73,
            rssi=22,
            transmission_mode='LOW_POWER_STANDARD_MODE',
            cloud_connectors=[
                disruptive.events.NetworkStatusCloudConnector(
                    device_id='123',
                    signal_strength=73,
                    rssi=22,
                ),
            ],
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_battery_status(self):
        x = disruptive.events.BatteryStatus(
            percentage=87,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_labels_changed(self):
        x = disruptive.events.LabelsChanged(
            added={'key1': 'value1', 'key2': 'value2'},
            modified={'key3': 'value3'},
            removed=['key4'],
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_connection_status(self):
        x = disruptive.events.ConnectionStatus(
            connection='ETHERNET',
            available=['ETHERNET', 'CELLULAR'],
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_ethernet_status(self):
        x = disruptive.events.EthernetStatus(
            mac_address='123',
            ip_address='abc',
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_cellular_status(self):
        x = disruptive.events.CellularStatus(
            signal_strength=88,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_co2(self):
        x = disruptive.events.Co2(
            ppm=300,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_pressure(self):
        x = disruptive.events.Pressure(
            pascal=700,
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_motion(self):
        x = disruptive.events.Motion(
            state='NO_MOTION_DETECTED',
            timestamp=datetime.now(),
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_desk_occupancy(self):
        x = disruptive.events.DeskOccupancy(
            state='OCCUPIED',
            timestamp=datetime.now(),
            remarks=['INCOMPLETE_DATA'],
        )

        y = eval(repr(x))
        assert x._raw == y._raw

    def test_contact(self):
        now = datetime.now()

        @dataclass
        class TestCase:
            state: str
            timestamp: datetime

        testcases = [
            TestCase(state='OPEN', timestamp=now),
            TestCase(state='CLOSED', timestamp=now),
        ]

        for testcase in testcases:
            x = disruptive.events.Contact(
                state=testcase.state,
                timestamp=testcase.timestamp,
            )

            y = eval(repr(x))
            assert x._raw == y._raw

    def test_probe_wire_status(self):
        now = datetime.now()

        @dataclass
        class TestCase:
            state: str
            timestamp: datetime

        testcases = [
            TestCase(state='INVALID_WIRE_CONFIGURATION', timestamp=now),
            TestCase(state='TWO_WIRE', timestamp=now),
            TestCase(state='THREE_WIRE', timestamp=now),
            TestCase(state='FOUR_WIRE', timestamp=now),
        ]

        for testcase in testcases:
            x = disruptive.events.ProbeWireStatus(
                state=testcase.state,
                timestamp=testcase.timestamp,
            )

            y = eval(repr(x))
            assert x._raw == y._raw
