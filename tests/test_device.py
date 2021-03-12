# Standard library imports.
import types

# Project imports.
import disruptive as dt

# Test imports.
import tests.mock_responses as mock_responses


class TestDevice():

    def test_attributes(self, request_mock):
        # Update the response data with device data.
        res = mock_responses.devices['touch']
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Assert attributes unpacked correctly.
        assert d.device_id == res['name'].split('/')[-1]
        assert d.type == res['type']

    def test_get(self, request_mock):
        # Update the response data with device data.
        request_mock.json = mock_responses.devices['touch']

        # Call the appropriate endpoint.
        d = dt.Device.get('project_id', 'device_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/devices/device_id',
        )

        # Assert attributes in output Device object.
        assert isinstance(d, dt.Device)

    def test_list(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = mock_responses.devices['list']

        # Call the appropriate endpoint.
        devices = dt.Device.list('project_id')

        # output should be list.
        assert type(devices) == list

        # Assert output instance.
        for d in devices:
            assert isinstance(d, dt.Device)

    def test_generator(self, request_mock):
        # Update the response data with a list of device data.
        request_mock.json = mock_responses.devices['list']

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
