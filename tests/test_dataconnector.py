# Project imports.
import disruptive as dt
from tests.framework import MockRequest, TestEndpoint
from tests.mock_responses import dataconnectors


class TestDataconnector(TestEndpoint):

    def test_get_expected(self):
        # Mock the REST API response with an expected dataconnector body.
        self.mock_request.return_value = MockRequest(
            json=dataconnectors['basic'],
        )

        # Send GET request for a single dataconnector in project.
        device = dt.Device.get('', '')

        # Assert that attributes in output object are as expected.
        assert device.id == dataconnectors['basic']['name'].split('/')[-1]
