# Standard library imports.
from unittest.mock import patch

# Third-party imports.
# import requests
from nose.tools import assert_raises

# Project imports.
import disruptive as dt
import disruptive.errors as errors


class TestResponseStatusCodes():
    @classmethod
    def setup_class(cls):
        cls.mock_request_patcher = patch('requests.request')
        cls.mock_request = cls.mock_request_patcher.start()

        # Initialise auth object to avoid unauthenticated error.
        # The credentials doesn't matter as we mock the request.
        dt.OAuth.authenticate('', '', '')

    @classmethod
    def teardown_class(cls):
        cls.mock_request_patcher.stop()

    def test_error_code_400(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 400

        # Call the service, which will send a request to the server.
        assert_raises(errors.BadRequest, dt.Device.get, '', '')

    def test_error_code_401(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 401

        # Call the service, which will send a request to the server.
        assert_raises(errors.Unauthenticated, dt.Device.get, '', '')

    def test_error_code_403(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 403

        # Call the service, which will send a request to the server.
        assert_raises(errors.Forbidden, dt.Device.get, '', '')

    def test_error_code_404(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 404

        # Call the service, which will send a request to the server.
        assert_raises(errors.NotFound, dt.Device.get, '', '')

    def test_error_code_409(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 409

        # Call the service, which will send a request to the server.
        assert_raises(errors.Conflict, dt.Device.get, '', '')

    def test_error_code_429(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 429

        # Call the service, which will send a request to the server.
        assert_raises(errors.TooManyRequests, dt.Device.get, '', '')

    def test_error_code_500(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 500

        # Call the service, which will send a request to the server.
        assert_raises(errors.InternalServerError, dt.Device.get, '', '')

    def test_error_code_503(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 503

        # Call the service, which will send a request to the server.
        assert_raises(errors.InternalServerError, dt.Device.get, '', '')

    def test_error_code_504(self):
        # Set response status code to represent test.
        self.mock_request.return_value.status_code = 504

        # Call the service, which will send a request to the server.
        assert_raises(errors.InternalServerError, dt.Device.get, '', '')
