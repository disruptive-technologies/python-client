import time
import urllib.parse

import jwt

import disruptive as dt
import disruptive.requests as req
import disruptive.errors as errors
from disruptive import transforms


class Auth():

    def __init__(self):
        # Initialise variables
        self.token = None

    def get_token(self):
        # Check expiration time.
        if self.has_expired():
            # Renew access token.
            self.refresh()

        return self.token

    def has_expired(self):
        raise errors.Unauthenticated(
            'Authentication object not initialized.\n\n\
            Set globally by calling one of the following methods:\n\
            Basic Auth: dt.BasicAuth.authorize(key_id, secret)\n\
            OAuth2:     dt.Oauth.authorize(key_id, secret, email)'
        )

    def _verify_str_credentials(self, credentials):
        for c in credentials:
            if type(c) != str:
                raise TypeError(
                    'Authentication credentials must be of type '
                    + '<class \'str\'>, but received {}.'.format(
                        type(c)
                    ))


class BasicAuth(Auth):
    def __init__(self, key_id, secret):
        # Inherit everything from parent.
        super().__init__()

        # Set initial variables.
        self._verify_str_credentials([key_id, secret])
        self.key_id = key_id
        self.secret = secret

        # Construct token.
        self.token = 'Basic {}'.format(
            transforms.base64_encode('{}:{}'.format(
                self.key_id,
                self.secret
            ))
        )

    @classmethod
    def authenticate(cls, key_id, secret):
        dt.auth = cls(key_id, secret)

    @classmethod
    def create(cls, key_id, secret):
        return cls(key_id, secret)

    def has_expired(self):
        return False


class OAuth(Auth):
    def __init__(self, key_id, secret, email):
        # Inherit everything from parent.
        super().__init__()

        # Verify str type and set input credential attributes.
        self._verify_str_credentials([key_id, secret, email])
        self.key_id = key_id
        self.secret = secret
        self.email = email

        # Initialise new attributes.
        self.expiration = 0

        # Run refresh once at initialization to set token.
        self.refresh()

    @classmethod
    def authenticate(cls, key_id, secret, email):
        dt.auth = cls(key_id, secret, email)

    @classmethod
    def create(cls, key_id, secret, email):
        return cls(key_id, secret, email)

    def __get_access_token(self):
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
            access_token_response = req.post(
                endpoint=token_url,
                data=request_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                authorize=False,
            )
        except errors.BadRequest:
            # Re-raise exception with more specific information.
            raise errors.BadRequest(
                'Could not authenticate with the provided credentials.\n'
                + 'Read more: https://developer.d21s.com/docs/authentication'
                + '/oauth2#common-errors'
            )

        # Return the access token in the request.
        return access_token_response

    def has_expired(self):
        if time.time() > self.expiration:
            return True
        else:
            return False

    def refresh(self):
        response = self.__get_access_token()
        self.expiration = time.time() + response['expires_in']
        self.token = 'Bearer {}'.format(response['access_token'])
