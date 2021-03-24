# Third-party imports.
import pytest

# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses
from disruptive.authentication import Auth


class TestAuth():

    def test_serviceaccount_auth(self, request_mock):
        # Update the response json with a mock token response.
        res = dtresponses.auth_token_fresh
        request_mock.json = res

        # Call the two classmethod constructors.
        auth = dt.Auth.serviceaccount('', '', '')

        # Assert token post request not sent at construction.
        request_mock.assert_request_count(0)

        # Assert instance of Auth class.
        assert isinstance(auth, Auth)

    def test_token_refresh(self, request_mock):
        # Update the response json with an expired token response.
        res = dtresponses.auth_token_expired
        request_mock.json = res

        # Create an authentication object.
        auth = dt.Auth.serviceaccount('', '', '')

        # Verify expired token.
        assert auth._has_expired()

        # Update the response json with a fresh token response.
        res = dtresponses.auth_token_fresh
        request_mock.json = res

        # Call the get_token method to force a refresh.
        auth.get_token()

        # Verify non-expired token.
        assert not auth._has_expired()

    def test_raise_missing_credential(self):
        # Verify TypeError raised at missing input credential.
        with pytest.raises(TypeError):
            dt.Auth.serviceaccount(None, '', '')
        with pytest.raises(TypeError):
            dt.Auth.serviceaccount('', None, '')
        with pytest.raises(TypeError):
            dt.Auth.serviceaccount('', '', None)
