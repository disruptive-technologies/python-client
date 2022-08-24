from __future__ import annotations

import os
import json
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
        If called, this function does nothing but raise an error as no
        authentication routine has been called to update the configuration
        variable, nor has an authentication object been provided.

        Raises
        ------
        Unauthorized
            If neither default_auth has been set nor the
            auth kwarg has been provided.

        """

        msg = 'Missing Service Account credentials.\n\n' \
            'Either set the following environment variables:\n\n' \
            '    DT_SERVICE_ACCOUNT_KEY_ID: Unique Service Account key ID.\n' \
            '    DT_SERVICE_ACCOUNT_SECRET: Unique Service Account secret.\n' \
            '    DT_SERVICE_ACCOUNT_EMAIL: Unique Service Account email.\n\n' \
            'or provide them programmatically:\n\n' \
            '    import disruptive as dt\n\n' \
            '    dt.default_auth = dt.Auth.service_account(\n' \
            '        key_id="<SERVICE_ACCOUNT_KEY_ID>",\n' \
            '        secret="<SERVICE_ACCOUNT_SECRET>",\n' \
            '        email="<SERVICE_ACCOUNT_EMAIL>",\n' \
            '    )\n\n' \
            'See https://developer.d21s.com/api/' \
            'libraries/python/client/authentication.html' \
            ' for more details.\n'

        raise dterrors.Unauthorized(msg)


class ServiceAccountAuth(_AuthRoutineBase):
    """
    Ensures that the access token is available and up-to-date.

    Attributes
    ----------
    token_endpoint : str
        URL to which the jwt is exchanged for an access token.

    """

    supported_algorithms = ['HS256']
    token_endpoint = 'https://identity.'\
        'disruptive-technologies.com/oauth2/token'

    def __init__(self, key_id: str, secret: str, email: str):
        # Inherit parent class methods and attributes.
        super().__init__()

        # Set parameter attributes.
        self._key_id: str = key_id
        self._secret: str = secret
        self._email: str = email

        # Default to HS256 algorithm.
        self._algorithm = self.supported_algorithms[0]

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

    @property
    def algorithm(self) -> str:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: str) -> None:
        if algorithm in self.supported_algorithms:
            self._algorithm = algorithm
        else:
            raise dterrors.ConfigurationError(
                f'unsupported algorithm {algorithm}'
            )

    @classmethod
    def from_credentials_file(cls, credentials: dict) -> ServiceAccountAuth:
        for key in ['keyId', 'secret', 'email', 'algorithm', 'tokenEndpoint']:
            if key not in credentials['serviceAccount']:
                raise dterrors.ConfigurationError(
                    f'Invalid credentials file. Missing field "{key}".'
                )

        cfg = credentials['serviceAccount']
        auth_obj = cls(
            key_id=cfg['keyId'],
            secret=cfg['secret'],
            email=cfg['email'],
        )
        auth_obj.algorithm = cfg['algorithm']
        auth_obj.token_endpoint = cfg['tokenEndpoint']

        return auth_obj

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
            'alg': self.algorithm,
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
            algorithm=self.algorithm,
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
            raise dterrors.Unauthorized(
                'Could not authenticate with the provided credentials.\n\n'
                'Read more: https://developer.d21s.com/docs/authentication'
                '/oauth2#common-errors'
            )

        # Return the access token in the request.
        return access_token_response


def _service_account_env_vars() -> Unauthenticated | ServiceAccountAuth:
    key_id = os.getenv('DT_SERVICE_ACCOUNT_KEY_ID', '')
    secret = os.getenv('DT_SERVICE_ACCOUNT_SECRET', '')
    email = os.getenv('DT_SERVICE_ACCOUNT_EMAIL', '')

    if '' in [key_id, secret, email]:
        return Unauthenticated()
    else:
        return Auth.service_account(key_id, secret, email)


def _credentials_file() -> Unauthenticated | ServiceAccountAuth:
    file_path = os.getenv('DT_CREDENTIALS_FILE')
    if file_path is not None:
        if not os.path.exists(file_path):
            msg = 'Missing credentials file.\n\n' \
                'Environment variable DT_CREDENTIALS_FILE is set, but' \
                ' no file found at target path.\n' \
                f'{file_path}'
            raise FileNotFoundError(msg)
        with open(file_path, 'r') as f:
            credentials = json.load(f)

        if 'serviceAccount' in credentials:
            return ServiceAccountAuth.from_credentials_file(credentials)

    return Unauthenticated()


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
    def init() -> Unauthenticated | ServiceAccountAuth:
        for method in [_credentials_file, _service_account_env_vars]:
            auth = method()
            if not isinstance(auth, Unauthenticated):
                return auth

        return Unauthenticated()

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

        Examples
        --------
        >>> # Authenticate using Service Account credentials.
        >>> dt.default_auth = dt.Auth.service_account(
        ...     key_id="<SERVICE_ACCOUNT_KEY_ID>",
        ...     secret="<SERVICE_ACCOUNT_KEY_ID>",
        ...     email="<SERVICE_ACCOUNT_KEY_ID>",
        ... )

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
