import disruptive as dt
from tests.framework import MockRequest, TestEndpoint
from tests.mock_responses import devices


class TestDevice(TestEndpoint):

    def test_get_minimal(self):
        self.mock_request.return_value = MockRequest(
            status_code=200,
            json=devices['touch'],
            headers={}
        )

        device = dt.Device.get('', '')

        assert device.id == devices['touch']['name'].split('/')[-1]
