from __future__ import annotations

import time
import urllib.parse
from typing import Any

import jwt

from disruptive import requests as dtrequests, errors as dterrors


class _AuthRoutineBase(object):

    def __init__(self) -> None:
        # Set default attributes.
        self._expiration: int = 0
        self._token: str = ''

    def _has_expired(self) -> bool:
        """
        Evaluates whether the access token has expired.

        Returns
        -------
        has_expired : bool
            True if the access token has expired, otherwise False.

        """

        if time.time() > self._expiration:
            return True
        else:
            return False

    def get_token(self) -> str:
        """
        Returns the access token.
        If the token has expired, renew it.

        Returns
        -------
        token : str
            Access token added to the request header.

        """

        # Check expiration time.
        if self._has_expired():
            # Renew access token.
            self.refresh()

        return self._token

    def refresh(self) -> None:
        """
        This function does nothing and is overwritten in all
        child classes. It only exists for consistency purposes
        as it is called in get_token().

        """

        pass


class Unauthenticated(_AuthRoutineBase):

    def __init__(self) -> None:
        # Inherit parent class methods and attributes.
        super().__init__()

    def refresh(self) -> None:
        """
        If called, this function does not but raise an error as no
        authentication routine has been called to update the configuration
        variable, nor has an authentication object been provided.

        Raises
        ------
        Unauthorized
            If neither default_auth has been set nor the
            auth kwarg has been provided.

        """
        raise dterrors.Unauthorized(
            'No authentication method set.'
            ' See developer.d21s.com/api/libraries/python/'
            'authentication.html'
        )


class ServiceAccountAuth(_AuthRoutineBase):
    """
    Ensures that the access token is available and up-to-date.

    Attributes
    ----------
    token_endpoint : str
        URL to which the jwt is exchanged for an access token.

    """

    def __init__(self, key_id: str, secret: str, email: str):
        # Inherit parent class methods and attributes.
        super().__init__()

        # Set parameter attributes.
        self._key_id: str = key_id
        self._secret: str = secret
        self._email: str = email

        # Set default URLs.
        self.token_endpoint = 'https://identity.'\
            'disruptive-technologies.com/oauth2/token'

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def secret(self) -> str:
        return self._secret

    @property
    def email(self) -> str:
        return self._email

    def __repr__(self) -> str:
        return '{}.{}({}, {}, {})'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            repr(self.key_id),
            repr(self.secret),
            repr(self.email),
        )

    def refresh(self) -> None:
        """
        Refreshes the access token.

        This first exchanges the JWT for an access token, then updates
        the expiration and token attributes with the response.

        """

        response: dict = self._get_access_token()
        self._expiration = time.time() + response['expires_in']
        self._token = 'Bearer {}'.format(response['access_token'])

    def _get_access_token(self) -> dict:
        """
        Constructs and exchanges the JWT for an access token.

        Returns
        -------
        response : dict
            Dictionary containing expiration and the token itself.

        Raises
        ------
        BadRequest
            If the provided credentials could not be used for authentication.

        """

        # Construct the JWT header.
        jwt_headers: dict[str, str] = {
            'alg': 'HS256',
            'kid': self.key_id,
        }

        # Construct the JWT payload.
        jwt_payload: dict[str, Any] = {
            'iat': int(time.time()),         # current unixtime
            'exp': int(time.time()) + 3600,  # expiration unixtime
            'aud': self.token_endpoint,
            'iss': self.email,
        }

        # Sign and encode JWT with the secret.
        encoded_jwt: str = jwt.encode(
            payload=jwt_payload,
            key=self.secret,
            algorithm='HS256',
            headers=jwt_headers,
        )

        # Prepare HTTP POST request data.
        # Note: The requests package applies Form URL-Encoding by default.
        request_data: str = urllib.parse.urlencode({
            'assertion': encoded_jwt,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        })

        # Exchange the JWT for an access token.
        try:
            access_token_response: dict = dtrequests.DTRequest.post(
                url='',
                base_url=self.token_endpoint,
                data=request_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                skip_auth=True,
            )
        except dterrors.BadRequest:
            # Re-raise exception with more specific information.
            raise dterrors.BadRequest(
                'Could not authenticate with the provided credentials.\n'
                'Read more: https://developer.d21s.com/docs/authentication'
                '/oauth2#common-errors'
            )

        # Return the access token in the request.
        return access_token_response


class Auth():
    """
    Authenticates the API using a factory design pattern.
    The Auth class itself is only for namespacing purposes.

    Depending on the classmethod called, an instance of some
    authentication routine, like ServiceAccountAuth, is returned.

    If no classmethod has been called, and the API is configured with
    an instance of the Auth class itself, exceptions will be raised
    with indicators on how to properly authenticate.

    """

    @staticmethod
    def unauthenticated() -> Unauthenticated:
        return Unauthenticated()

    @classmethod
    def service_account(cls,
                        key_id: str,
                        secret: str,
                        email: str,
                        ) -> ServiceAccountAuth:
        """
        This method uses an OAuth2 authentication flow. With the provided
        credentials, a `JWT <https://jwt.io/>`_ is created and exchanged for
        an access token.

        Parameters
        ----------
        key_id : str
            Unique Service Account key ID.
        secret : str
            Service Account secret.
        email : str
            Unique Service Account email address.

        Returns
        -------
        auth : ServiceAccountAuth
            Object to initialize and maintain authentication to the REST API.

        """

        # Check that credentials are populated strings.
        cls._verify_str_credentials({
            'key_id': key_id,
            'secret': secret,
            'email': email,
        })

        return ServiceAccountAuth(key_id, secret, email)

    @staticmethod
    def _verify_str_credentials(credentials: dict) -> None:
        """
        Verifies that the provided credentials are strings.

        This check is added as people use environment variables, but
        if for instance os.environ.get() does not find one, it silently
        returns None. It's better to just check for it early.

        Parameters
        ----------
        credentials : dict
            Credentials used to authenticate the REST API.

        """

        for key in credentials:
            # Verify credential is type string.
            if isinstance(credentials[key], str):
                # Raise ConfigurationError if string is empty.
                # This typically happens is credentials are fetched from
                # the environment with a fallback to an empty string.
                if len(credentials[key]) == 0:
                    raise dterrors.ConfigurationError(
                        'Authentication credential <{}> is'
                        ' empty string.'.format(key)
                    )

            # If not, raise TypeError.
            else:
                raise dterrors._raise_builtin(
                    TypeError,
                    'Authentication credential <{}> got type <{}>. '
                    'Expected <str>.'.format(
                        key, type(credentials[key]).__name__
                    )
                )
