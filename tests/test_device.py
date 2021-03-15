# Standard library imports.
import types

# Project imports.
import disruptive as dt
import disruptive.events as dtevents
import disruptive.datas as dtdatas
import tests.mock_responses as dtresponses


class TestDevice():

    def test_unpack(self, request_mock):
        # Update the response data with device data.
        res = dtresponses.touch_sensor
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Assert attributes unpacked correctly.
        assert d.device_id == res['name'].split('/')[-1]
        assert d.type == res['type']

    def test_get(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtresponses.touch_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/devices/device_id',
        )

        # Assert instance of Device object.
        assert isinstance(d, dt.Device)

    def test_list(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtresponses.paginated_device_response

        # Call the appropriate endpoint.
        devices = dt.Device.list('project_id')

        # output should be list.
        assert type(devices) == list

        # Assert output instance for devices in list.
        for d in devices:
            assert isinstance(d, dt.Device)

    def test_generator(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtresponses.paginated_device_response

        # Call the appropriate endpoint.
        gen = dt.Device.generator('project_id')

        # Assert function returns a generator.
        assert isinstance(gen, types.GeneratorType)

        # Assert generator output is as expected.
        for page in gen:
            # Each page should be a list.
            assert type(page) == list
            # Iterate devices in page list.
            for device in page:
                # Each device should be an instance of Device.
                assert isinstance(device, dt.Device)

    def test_no_reported_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtresponses.null_reported_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Assert None for all reported datas.
        for key in dtevents.EVENTS_MAP:
            attr = dtevents.EVENTS_MAP[key]['attr']
            assert getattr(d.reported, attr) is None

    def test_reported_touch_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtresponses.touch_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Assert appropriate reported data instances.
        assert isinstance(d.reported.network_status, dtdatas.NetworkStatus)
        assert isinstance(d.reported.battery_status, dtdatas.BatteryStatus)
        assert isinstance(d.reported.touch, dtdatas.Touch)
