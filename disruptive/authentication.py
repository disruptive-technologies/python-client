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
    """
    Parent class for authenticating the REST API.

    Attributes
    ----------
    token : str
        Access token added to the request header.

    """

    def __init__(self) -> None:
        """
        Constructs the Auth object by initializing token to empty string.

        Parameters
        ----------
        project : dict
            Unmodified project response dictionary.

        """

        # Initialise attributes.
        self.token = ''

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
        if self.has_expired():
            # Renew access token.
            self.refresh()

        return self.token

    def refresh(self) -> None:
        """
        This function only exists as a placeholder for when unauthenticated
        and should never be called until authentication has been set up.
        Once authenticated it will be overwritten by the child class.
        """
        pass

    def has_expired(self) -> bool:
        """
        Raises an Unauthenticated error with some added information.
        If this function is called, the project has not yet been
        authenticated, and the user should be reminded to do so.

        """
        raise dterrors.Unauthenticated(
            'Authentication object not initialized.\n\n\
            Set globally by calling one of the following methods:\n\
            Basic Auth: dt.Auth.basic(key_id, secret)\n\
            OAuth2:     dt.Auth.oauth(key_id, secret, email)'
        )

    def _verify_str_credentials(self, credentials: list[str]) -> None:
        """
        Verifies that the provided credentials are strings.

        This check is added as people use environment variables, but
        if for instance os.environ.get() does not find one, it silently
        returns None. It's better to just check for it early.

        Parameters
        ----------
        credentials : list[str]
            List of credentials used to initialize the authentication routine.

        """

        for c in credentials:
            if type(c) != str:
                raise TypeError(
                    'Authentication credentials must be of type '
                    + '<class \'str\'>, but received {}.'.format(
                        type(c)
                    ))


class BasicAuth(Auth):
    """
    Class for authenticating the REST API using Basic Auth scheme.

    Attributes
    ----------
    token : str
        Access token added to the request header.
    key_id : str
        Service Account Key ID.
    secret : str
        Service Account secret.

    """

    def __init__(self, key_id: str, secret: str) -> None:
        """
        Constructs the BasicAuth object by inheriting parent, then
        constructing the token from the provided credentials.

        Parameters
        ----------
        key_id : str
            Service Account Key ID.
        secret : str
            Service Account secret.

        """

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
        """
        Returns False as Basic Auth token is static
        and does not need to be refreshed.

        Returns
        -------
        false : bool
            Always returns False.

        """
        return False


class OAuth(Auth):
    """
    Class for authenticating the REST API using an OAuth2 scheme.

    Attributes
    ----------
    token : str
        Access token added to the request header.
    key_id : str
        Service Account Key ID.
    secret : str
        Service Account secret.
    email : str
        Service Account email address.
    expiration : int
        Unixtime of when the access token expires.

    """

    def __init__(self, key_id: str, secret: str, email: str) -> None:
        """
        Constructs the OAuth object by inheriting parent, then
        initializing attributes needed for refresh scheme later.

        Parameters
        ----------
        key_id : str
            Service Account Key ID.
        secret : str
            Service Account secret.
        email : str
            Service Account email address.

        """

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

    def refresh(self) -> None:
        """
        Refreshes the access token.

        This first exchanges the JWT for an access token, then updates
        the expiration and token attributes with the response.

        """

        response = self.__get_access_token()
        self.expiration = time.time() + response['expires_in']
        self.token = 'Bearer {}'.format(response['access_token'])
