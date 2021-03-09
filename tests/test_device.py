# Project imports.
import disruptive as dt
from tests.framework import MockRequest, TestEndpoint
from tests.mock_responses import devices


class TestDevice(TestEndpoint):

    def test_get_expected(self):
        # Mock the REST API response with an expected device body.
        self.mock_request.return_value = MockRequest(
            json=devices['touch'],
        )

        # Send GET request for a single device in project.
        device = dt.Device.get('', '')

        # Assert that attributes in output object are as expected.
        assert device.id == devices['touch']['name'].split('/')[-1]
