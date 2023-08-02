from unittest.mock import patch

import disruptive
import disruptive.events.events as dtevents
import tests.api_responses as dtapiresponses
import disruptive.errors as dterrors


class TestDevice():

    def test_repr(self, request_mock):
        # Update the response data with device data.
        res = dtapiresponses.touch_sensor
        request_mock.json = res

        # Fetch a device.
        x = disruptive.Device.get_device('device_id', 'project_id')

        # Evaluate __repr__ function and compare copy.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_unpack(self, request_mock):
        # Update the response data with device data.
        res = dtapiresponses.touch_sensor
        request_mock.json = res

        # Call the appropriate endpoint.
        d = disruptive.Device.get_device('device_id', 'project_id')

        # Assert attributes unpacked correctly.
        assert d.device_id == res['name'].split('/')[-1]
        assert d.device_type == res['type']

    def test_get_device(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.touch_sensor

        # Call Device.get_device() method.
        d = disruptive.Device.get_device('device_id', 'project_id')

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instance of Device object.
        assert isinstance(d, disruptive.Device)

    def test_get_device_project_wildcard(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.touch_sensor

        # Call Device.get_device() method without providing project_id.
        d = disruptive.Device.get_device(device_id='device_id')

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/-/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instance of Device object.
        assert isinstance(d, disruptive.Device)

    def test_list_devices(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtapiresponses.paginated_device_response

        # Call Device.list_devices() method.
        devices = disruptive.Device.list_devices('project_id')

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/devices'
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
            assert isinstance(d, disruptive.Device)

    def test_list_devices_optionals(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = dtapiresponses.paginated_device_response

        # Call Device.list_devices() method.
        devices = disruptive.Device.list_devices(
            project_id='project_id',
            query='some_filter',
            device_ids=['device1, device2'],
            device_types=['temperature'],
            label_filters={'key': 'value'},
            order_by='reported.temperature.value',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/devices'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={
                'query': 'some_filter',
                'device_ids': ['device1, device2'],
                'device_types': ['temperature'],
                'order_by': 'reported.temperature.value',
                'label_filters': ['key=value'],
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # output should be list.
        assert type(devices) == list

        # Assert output is list of Device.
        for d in devices:
            assert isinstance(d, disruptive.Device)

    def test_batch_update_labels(self, request_mock):
        # Update the response data with labelupdate response data.
        request_mock.json = dtapiresponses.batch_label_response

        # Call Device.batch_update_labels() method.
        d = disruptive.Device.batch_update_labels(
            device_ids=['device_id1', 'device_id2', 'device_id3'],
            project_id='project_id',
            set_labels={
                'key1': 'value1',
                'key2': 'value2',
            },
            remove_labels=['remove-key'],
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/devices:batchUpdate'
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
        assert isinstance(d, list)

    def test_set_label(self, request_mock):
        # Update the response data with labelupdate response data.
        request_mock.json = dtapiresponses.batch_label_response

        # Call Device.set_label() method.
        d = disruptive.Device.set_label(
            device_id='device_id',
            project_id='project_id',
            key='key',
            value='value',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/devices:batchUpdate'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'devices': [
                    'projects/project_id/devices/device_id',
                ],
                'addLabels': {'key': 'value'},
            },
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert isinstance(d, list)

    def test_remove_label(self, request_mock):
        # Update the response data with labelupdate response data.
        request_mock.json = dtapiresponses.batch_label_response

        # Call Device.remove_label() method.
        d = disruptive.Device.remove_label(
            device_id='device_id',
            project_id='project_id',
            key='key',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/devices:batchUpdate'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'devices': [
                    'projects/project_id/devices/device_id',
                ],
                'removeLabels': ['key'],
            },
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert isinstance(d, list)

    def test_transfer_devices(self, request_mock):
        # Update the response data with transfer response data.
        request_mock.json = dtapiresponses.transfer_device_no_errors

        # Call Device.remove_label() method.
        d = disruptive.Device.transfer_devices(
            device_ids=['device_id1', 'device_id2'],
            source_project_id='source_project',
            target_project_id='target_project',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/target_project/devices:transfer'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'devices': [
                    'projects/source_project/devices/device_id1',
                    'projects/source_project/devices/device_id2',
                ],
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output.
        assert isinstance(d, list)
        assert len(d) == 0

    def test_transfer_devices_errors(self, request_mock):
        # Update the response data with transfer response data.
        request_mock.json = dtapiresponses.transfer_device_errors

        # Define device ids to transfer.
        good_ids = ['device_id1', 'device_id2']
        bad_ids = ['abc', '123']

        # Call Device.remove_label() method.
        d = disruptive.Device.transfer_devices(
            device_ids=good_ids+bad_ids,
            source_project_id='source_project',
            target_project_id='target_project',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/target_project/devices:transfer'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'devices': [
                    'projects/source_project/devices/device_id1',
                    'projects/source_project/devices/device_id2',
                    'projects/source_project/devices/abc',
                    'projects/source_project/devices/123',
                ],
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output.
        assert isinstance(d, list)
        assert len(d) == 2
        for e in d:
            # List should contain TransferDeviceError.
            assert isinstance(e, dterrors.TransferDeviceError)

            # Id should be one of the bad ones.
            assert e.device_id in bad_ids
            assert e.device_id not in good_ids

    def test_reported_no_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.null_reported_sensor

        # Call the appropriate endpoint.
        d = disruptive.Device.get_device('device_id', 'project_id')

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
        d = disruptive.Device.get_device('device_id', 'project_id')

        # Assert appropriate reported data instances.
        assert isinstance(d.reported.network_status, dtevents.NetworkStatus)
        assert isinstance(d.reported.battery_status, dtevents.BatteryStatus)
        assert isinstance(d.reported.touch, dtevents.Touch)

    def test_reported_unknown_data(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.unknown_reported_sensor

        # Mock the warning logger.
        with patch('disruptive.logging.warning') as warning_mock:
            # Call the appropriate endpoint.
            disruptive.Device.get_device('device_id', 'project_id')

            assert warning_mock.call_count == 1

    def test_missing_product_number(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtapiresponses.null_reported_sensor

        # Call Device.get_device() method.
        d = disruptive.Device.get_device('device_id', 'project_id')

        # Verify expected outgoing parameters in request.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instance of Device object.
        assert isinstance(d, disruptive.Device)

        # Assert empty string as product number.
        assert d.product_number == ''

    def test_reported_constructor(self):
        events = [
            dtapiresponses.touch_event,
            dtapiresponses.temperature_event,
            dtapiresponses.object_present_event,
            dtapiresponses.humidity_event,
            dtapiresponses.object_present_count_event,
            dtapiresponses.touch_count_event,
            dtapiresponses.water_present_event,
            dtapiresponses.network_status_event,
            dtapiresponses.battery_status_event,
            dtapiresponses.labels_changed_event,
            dtapiresponses.connection_status_event,
            dtapiresponses.ethernet_status_event,
            dtapiresponses.cellular_status_event,
            dtapiresponses.co2_event,
            dtapiresponses.motion_event,
            dtapiresponses.pressure_event,
        ]

        for event in events:
            device_dict = dtapiresponses.temperature_sensor
            device_dict['reported'] = event['data']
            _ = disruptive.Device(device_dict)
