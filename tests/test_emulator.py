# Project imports.
import disruptive as dt
import tests.api_responses as dtapiresponses


class TestEmulator():

    def test_create_device(self, request_mock):
        # Update the response data with device data.
        res = dtapiresponses.created_temperatur_emulator
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
            url=dt.emulator_url+'/projects/project_id/devices',
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
            url=dt.emulator_url+'/projects/project_id/devices/device_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert d is None

    def test_publish_event(self, request_mock):
        # Call Emulator.publish_event() method.
        d = dt.Emulator.publish_event(
            device_id='device_id',
            project_id='project_id',
            data=dt.events.Temperature(
                celsius=55,
                timestamp='1970-01-01T00:00:00Z',
            ),
        )

        # Verify expected outgoing parameters in request.
        url = dt.emulator_url
        url += '/projects/project_id/devices/device_id:publish'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'temperature': {
                    'value': 55,
                    'updateTime': '1970-01-01T00:00:00Z',
                }
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert d is None