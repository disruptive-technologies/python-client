from __future__ import annotations

# Standard library imports.
import time
import urllib.parse

# Third-party imports.
import jwt

# Project imports
import disruptive.requests as dtrequests
import disruptive.errors as dterrors


class Auth():

    def __init__(self, method: str, credentials: dict[str, str]) -> None:
        # Verify provided credentials are strings.
        self._verify_str_credentials(credentials)

        # Initialize attributes with nonset values.
        self.token = ''
        self.expiration = 0

        # Set arguments as attributes
        self.method = method
        self.credentials = credentials

    @classmethod
    def serviceaccount(cls,
                       key_id: str,
                       secret: str,
                       email: str,
                       ) -> Auth:
        # Construct Auth object with method and credentials.
        obj = cls(
            method='serviceaccount',
            credentials={
                'key_id': key_id,
                'secret': secret,
                'email': email,
            },
        )

        # Patch the newly created object with method-specific methods.
        setattr(obj, '_has_expired', obj.__serviceaccount_has_expired)
        setattr(obj, 'refresh', obj.__serviceaccount_refresh)

        # Return the patch object.
        return obj

    def _verify_str_credentials(self, credentials: dict) -> None:
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
            if type(credentials[key]) != str:
                raise TypeError(
                    'Authentication credentials must be of type '
                    + '<class \'str\'>, but received {}.'.format(
                        type(credentials[key])
                    ))

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

        return self.token

    def _has_expired(self) -> bool:
        """
        Raises an Unauthenticated error with some added information.
        If this function is called, the project has not yet been
        authenticated, and the user should be reminded to do so.

        """
        raise dterrors.Unauthenticated(
            {
                'code': None,
                'error': 'No authentication method has been provided.',
                'help': 'You can authenticate once for all endpoints:'
                + '\n>>> import disruptive as dt'
                + '\n>>> dt.auth = dt.Auth.serviceaccount'
                + '(key_id, secret, email)'
                + '\n\nOr authenticate each endpoint individually:'
                + '\n>>> import disruptive as dt'
                + '\n>>> dt.Resource.method(_, auth=dt.Auth.serviceaccount'
                + '(key_id, secret, email))'
                + '\n\nThe following authentication methods are available:'
                + '\n>>> dt.Auth.serviceaccount'
                + '(key_id, secret, email)'
            }
        )

    def refresh(self) -> None:
        """
        This function does nothing until an authenticate method has
        been initialized. Until then, it acts as a name placeholder
        which is replaced by a type-specific method.
        """
        pass

    def __serviceaccount_has_expired(self) -> bool:
        """
        Evaluates whether the access token has expired.

        Returns
        -------
        has_expired : bool
            True if the access token has expired, otherwise False.

        """

        if time.time() > self.expiration:
            return True
        else:
            return False

    def __serviceaccount_refresh(self) -> None:
        """
        Refreshes the access token.

        This first exchanges the JWT for an access token, then updates
        the expiration and token attributes with the response.

        """

        response = self.__serviceaccount_get_access_token()
        self.expiration = time.time() + response['expires_in']
        self.token = 'Bearer {}'.format(response['access_token'])

    def __serviceaccount_get_access_token(self) -> dict:
        """
        Constructs and exchanges the JWT for an access token.

        Returns
        -------
        response : dict
            Dictionary containing expiration and the token itself.

        """

        # Set access token URL.
        token_url = 'https://identity.disruptive-technologies.com/oauth2/token'

        # Construct the JWT header.
        jwt_headers = {
            'alg': 'HS256',
            'kid': self.credentials['key_id'],
        }

        # Construct the JWT payload.
        jwt_payload = {
            'iat': int(time.time()),         # current unixtime
            'exp': int(time.time()) + 3600,  # expiration unixtime
            'aud': token_url,
            'iss': self.credentials['email'],
        }

        # Sign and encode JWT with the secret.
        encoded_jwt = jwt.encode(
            payload=jwt_payload,
            key=self.credentials['secret'],
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
