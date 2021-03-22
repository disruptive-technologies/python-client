from __future__ import annotations

# Standard library imports.
import time
import urllib.parse

# Third-party imports.
import jwt

# Project imports
import disruptive.requests as dtrequests
import disruptive.errors as dterrors
import disruptive.transforms as dttrans


class Auth():

    def __init__(self) -> None:
        # Initialise variables
        self.token = ''

    def get_token(self) -> str:
        # Check expiration time.
        if self.has_expired():
            # Renew access token.
            self.refresh()

        return self.token

    def refresh(self) -> None:
        # This function only exists to please Mypy type-checking.
        # If unauthorized, it should never be called.
        # Once authorized, it will be overwritten by the child class.
        pass

    def has_expired(self) -> bool:
        raise dterrors.Unauthenticated(
            'Authentication object not initialized.\n\n\
            Set globally by calling one of the following methods:\n\
            Basic Auth: dt.Auth.basic(key_id, secret)\n\
            OAuth2:     dt.Auth.oauth(key_id, secret, email)'
        )

    def _verify_str_credentials(self, credentials: list[str]) -> None:
        for c in credentials:
            if type(c) != str:
                raise TypeError(
                    'Authentication credentials must be of type '
                    + '<class \'str\'>, but received {}.'.format(
                        type(c)
                    ))


class BasicAuth(Auth):

    def __init__(self, key_id: str, secret: str) -> None:
        # Inherit everything from parent.
        super().__init__()

        # Set initial variables.
        self._verify_str_credentials([key_id, secret])
        self.key_id = key_id
        self.secret = secret

        # Construct token.
        self.token = 'Basic {}'.format(
            dttrans.base64_encode('{}:{}'.format(
                self.key_id,
                self.secret
            ))
        )

    def has_expired(self) -> bool:
        return False


class OAuth(Auth):

    def __init__(self, key_id: str, secret: str, email: str) -> None:
        # Inherit everything from parent.
        super().__init__()

        # Verify str type and set input credential attributes.
        self._verify_str_credentials([key_id, secret, email])
        self.key_id = key_id
        self.secret = secret
        self.email = email

        # Initialise new attributes.
        self.expiration = 0

    def __get_access_token(self) -> dict:
        # Set access token URL.
        token_url = 'https://identity.disruptive-technologies.com/oauth2/token'

        # Construct the JWT header.
        jwt_headers = {
            'alg': 'HS256',
            'kid': self.key_id,
        }

        # Construct the JWT payload.
        jwt_payload = {
            'iat': int(time.time()),         # current unixtime
            'exp': int(time.time()) + 3600,  # expiration unixtime
            'aud': token_url,
            'iss': self.email,
        }

        # Sign and encode JWT with the secret.
        encoded_jwt = jwt.encode(
            payload=jwt_payload,
            key=self.secret,
            algorithm='HS256',
            headers=jwt_headers,
        )

        # Prepare HTTP POST request data.
        # Note: The requests package applies Form URL-Encoding by default.
        request_data = urllib.parse.urlencode({
            'assertion': encoded_jwt,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        })

        # Exchange the JWT for an access token.
        try:
            access_token_response = dtrequests.post(
                url=token_url,
                data=request_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                authorize=False,
            )
        except dterrors.BadRequest:
            # Re-raise exception with more specific information.
            raise dterrors.BadRequest(
                'Could not authenticate with the provided credentials.\n'
                + 'Read more: https://developer.d21s.com/docs/authentication'
                + '/oauth2#common-errors'
            )

        # Return the access token in the request.
        return access_token_response

    def has_expired(self) -> bool:
        if time.time() > self.expiration:
            return True
        else:
            return False

    def refresh(self) -> None:
        response = self.__get_access_token()
        self.expiration = time.time() + response['expires_in']
        self.token = 'Bearer {}'.format(response['access_token'])
