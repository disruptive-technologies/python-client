# Project imports.
import disruptive as dt

# Test imports.
import tests.mock_responses as mock_responses


class TestDevice():

    def test_attributes(self, request_mock):
        # Mock the REST API response with an expected device body.
        res = mock_responses.devices['touch']
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.Device.get('project-id', 'device-id')

        # Assert attributes unpacked correctly.
        assert d.id == res['name'].split('/')[-1]
        assert d.type == res['type']

    def test_get(self, request_mock):
        # Mock the REST API response with an expected device body.
        request_mock.json = mock_responses.devices['touch']

        # Call the appropriate endpoint.
        d = dt.Device.get('project-id', 'device-id')

        # Assert attributes in output Device object.
        assert isinstance(d, dt.Device)

    def test_list(self, request_mock):
        # Mock the REST API response with an expected device body.
        request_mock.json = mock_responses.devices['list']

        # Call the appropriate endpoint.
        devices = dt.Device.list('project-id')

        # Assert output instance.
        for d in devices:
            assert isinstance(d, dt.Device)
