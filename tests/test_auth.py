# Standard library imports.
from unittest.mock import patch

# Third-party imports.
import pytest

# Project imports.
import disruptive as dt


class TestOAuth():

    def test_constructors(self):
        # Mock POST request wrapper response.
        with patch('disruptive.requests.post') as mock_auth_post:
            mock_auth_post.return_value = {
                'access_token': '',
                'expires_in': 3600,
            }

            # Call the two classmethod constructors.
            dt.OAuth.authenticate('', '', '')
            dt.OAuth.create('', '', '')

    def test_token_refresh(self):
        # Mock POST request wrapper response with expired token.
        with patch('disruptive.requests.post') as mock_auth_post:
            mock_auth_post.return_value = {
                'access_token': '',
                'expires_in': 0,
            }

            # Create an authentication object.
            auth = dt.OAuth.create('', '', '')

        # Verify expired token.
        assert auth.has_expired()

        # Mock POST request wrapper response with updated expiration.
        with patch('disruptive.requests.post') as mock_auth_post:
            mock_auth_post.return_value = {
                'access_token': '',
                'expires_in': 3600,
            }

            # Call the get_token method to force a refresh.
            auth.get_token()

        # Verify non-expired token.
        assert not auth.has_expired()

    def test_raise_missing_credential(self):
        # Verify TypeError raised at missing input credential.
        with pytest.raises(TypeError):
            dt.OAuth.authenticate(None, '', '')
        with pytest.raises(TypeError):
            dt.OAuth.authenticate('', None, '')
        with pytest.raises(TypeError):
            dt.OAuth.authenticate('', '', None)
