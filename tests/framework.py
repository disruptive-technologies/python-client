from unittest.mock import patch

import disruptive as dt


class MockRequest():

    def __init__(self, status_code=200, json={}, headers={}):
        self.status_code = status_code
        self.headers = headers
        self._json = json

    def json(self):
        return self._json


class TestEndpoint():

    @classmethod
    def setup_class(cls):
        cls.mock_request_patcher = patch('disruptive.requests.__send_request')
        cls.mock_request = cls.mock_request_patcher.start()

        # Initialize the authorisation object to avoid Unauthorized error.
        with patch('disruptive.requests.post') as mock_auth_post:
            mock_auth_post.return_value = {
                'access_token': '',
                'expires_in': 3600,
            }
            dt.OAuth.authenticate('', '', '')

    @classmethod
    def teardown_class(cls):
        cls.mock_request_patcher.stop()
