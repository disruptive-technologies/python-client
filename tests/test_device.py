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

        # Call Device.get_device() method.
        d = dt.Device.get_device('device_id', 'project_id')

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/projects/project_id/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instance of Device object.
        assert isinstance(d, dt.Device)

    def test_list_devices(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtapiresponses.paginated_device_response

        # Call Device.list_devices() method.
        devices = dt.Device.list_devices('project_id')

        # Verify expected outgoing parameters in request.
        url = dt.api_url+'/projects/project_id/devices'
        request_mock.assert_requested(
            method='GET',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # output should be list.
        assert type(devices) == list

        # Assert output is list of Device.
        for d in devices:
            assert isinstance(d, dt.Device)

    def test_batch_update_labels(self, request_mock):
        # Call Device.batch_update_labels() method.
        d = dt.Device.batch_update_labels(
            device_ids=['device_id1', 'device_id2', 'device_id3'],
            project_id='project_id',
            set_labels={
                'key1': 'value1',
                'key2': 'value2',
            },
            remove_labels=['remove-key'],
        )

        # Verify expected outgoing parameters in request.
        url = dt.api_url+'/projects/project_id/devices:batchUpdate'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'devices': [
                    'projects/project_id/devices/device_id1',
                    'projects/project_id/devices/device_id2',
                    'projects/project_id/devices/device_id3',
                ],
                'addLabels': {'key1': 'value1', 'key2': 'value2'},
                'removeLabels': ['remove-key'],
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert d is None

    def test_no_reported_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.null_reported_sensor

        # Call the appropriate endpoint.
        d = dt.Device.get_device('device_id', 'project_id')

        # Assert None for all reported datas.
        for key in dtevents._EVENTS_MAP._api_names:
            # Skip labelsChanged as it does not exist in reported.
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
