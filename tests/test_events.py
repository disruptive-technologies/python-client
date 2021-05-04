from datetime import datetime

import disruptive


class TestEvents():

    def test_touch(self):
        # Construct Touch Event.
        x = disruptive.events.Touch(timestamp=datetime.now())

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_temperature(self):
        # Construct Touch Event.
        x = disruptive.events.Temperature(
            celsius=23,
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_object_present(self):
        # Construct Touch Event.
        x = disruptive.events.ObjectPresent(
            state='PRESENT',
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_humidity(self):
        # Construct Touch Event.
        x = disruptive.events.Humidity(
            celsius=23,
            humidity=99.9,
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_object_present_count(self):
        # Construct Touch Event.
        x = disruptive.events.ObjectPresentCount(
            total=9791,
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_touch_count(self):
        # Construct Touch Event.
        x = disruptive.events.TouchCount(
            total=183,
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_water_present(self):
        # Construct Touch Event.
        x = disruptive.events.WaterPresent(
            state='NOT_PRESENT',
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_network_status(self):
        # Construct Touch Event.
        x = disruptive.events.NetworkStatus(
            signal_strength=73,
            rssi=22,
            transmission_mode='LOW_POWER_STANDARD_MODE',
            cloud_connectors=[
                disruptive.events.NetworkStatusCloudConnector(
                    cloudconnector_id='123',
                    signal_strength=73,
                    rssi=22,
                ),
            ],
            timestamp=datetime.now(),
        )

        # Evaluate repr.
        y = eval(repr(x))
        assert x._raw == y._raw
