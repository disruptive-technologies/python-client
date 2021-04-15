# Project imports.
import disruptive as dt
import disruptive.events.events as dtevents
import tests.api_responses as dtapiresponses


class TestDevice():

    def test_unpack(self, request_mock):
        # Update the response data with device data.
        res = dtapiresponses.touch_sensor
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.Device.get_device('device_id', 'project_id')

        # Assert attributes unpacked correctly.
        assert d.device_id == res['name'].split('/')[-1]
        assert d.type == res['type']

    def test_get_device(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.touch_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get_device('device_id', 'project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/projects/project_id/devices/device_id',
        )

        # Assert instance of Device object.
        assert isinstance(d, dt.Device)

    def test_list_devices(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtapiresponses.paginated_device_response

        # Call the appropriate endpoint.
        devices = dt.Device.list_devices('project_id')

        # output should be list.
        assert type(devices) == list

        # Assert output instance for devices in list.
        for d in devices:
            assert isinstance(d, dt.Device)

    def test_no_reported_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.null_reported_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get_device('device_id', 'project_id')

        # Assert None for all reported datas.
        for key in dtevents._EVENTS_MAP._api_names:
            # Skip labelsChanged
            if key == 'labelsChanged':
                continue

            attr = dtevents._EVENTS_MAP._api_names[key].attr_name
            assert getattr(d.reported, attr) is None

    def test_reported_touch_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.touch_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get_device('device_id', 'project_id')

        # Assert appropriate reported data instances.
        assert isinstance(d.reported.network_status, dtevents.NetworkStatus)
        assert isinstance(d.reported.battery_status, dtevents.BatteryStatus)
        assert isinstance(d.reported.touch, dtevents.Touch)
