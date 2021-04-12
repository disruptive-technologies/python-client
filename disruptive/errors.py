import requests
from disruptive.responses import DTResponse


class DTApiError(Exception):
    """
    Represents errors raised from the REST API.

    """

    def __init__(self, message):

        # Call the base class constructor.
        super().__init__(message)


class BadRequest(DTApiError):
    """
    The response contained a status code of 400.
    https://developer.d21s.com/docs/error-codes#400

    """

    def __init__(self, message):
        super().__init__(message)


class Unauthorized(DTApiError):
    """
    The response contained a status code of 401.
    https://developer.d21s.com/docs/error-codes#401

    """

    def __init__(self, message):
        super().__init__(message)


class Forbidden(DTApiError):
    """
    The response contained a status code of 403.
    https://developer.d21s.com/docs/error-codes#403

    """

    def __init__(self, message):
        super().__init__(message)


class NotFound(DTApiError):
    """
    The response contained a status code of 404.
    https://developer.d21s.com/docs/error-codes#404

    """

    def __init__(self, message):
        super().__init__(message)


class Conflict(DTApiError):
    """
    The response contained a status code of 409.
    https://developer.d21s.com/docs/error-codes#409

    """

    def __init__(self, message):
        super().__init__(message)


class TooManyRequests(DTApiError):
    """
    The response contained a status code of 429.
    https://developer.d21s.com/docs/error-codes#429

    """

    def __init__(self, message):
        super().__init__(message)


class InternalServerError(DTApiError):
    """
    The response contained a status code of 500.
    https://developer.d21s.com/docs/error-codes#500

    """

    def __init__(self, message):
        super().__init__(message)


class ReadTimeout(DTApiError):
    """
    The server did not respond in the alloted amount
    of time set by :ref:`request_timeout <config params>`.

    """

    def __init__(self, message):
        super().__init__(message)


class ConnectionError(DTApiError):
    """
    Could not establish connection to the server.

    """

    def __init__(self, message):
        super().__init__(message)


class FormatError(DTApiError):
    """
    Some string formatting, usually a timestamp, is wrong.

    """

    def __init__(self, message):
        super().__init__(message)


class ConfigurationError(DTApiError):
    """
    One or more :ref:`configuration parameters <configuration>` are invalid.

    """

    def __init__(self, message):
        super().__init__(message)


class UnknownError(DTApiError):
    """
    An unexpected error has been raised.

    This is likely due to a bug in the package.
    Please report this to developer-support@disruptive-technologies.com.

    """

    def __init__(self, message):
        super().__init__(message)


# Parses the status code, and returns (error, should_retry, retry_after)
def parse_error(res: DTResponse, retry_count: int):
    """
    Evaluates the status code and returns instructions for
    how to deal with the error in a request.

    Parameters
    ----------
    DTResponse : DTResponse
        A DTResponse object containing body, status_code and a help message.
    retry_count : int
        Current retry attempt.

    Returns
    -------
    tuple : tuple
        The error to be raised, a bool whether to retry the request, and
        an int defining how long to wait before retrying.

    """

    # Check for arleady caught errors.
    if res.caught_error is not None:
        if isinstance(res.caught_error, requests.exceptions.ReadTimeout):
            return (ReadTimeout, True, retry_count**2)
        elif isinstance(res.caught_error, requests.exceptions.ConnectionError):
            return (
                ConnectionError('Failed to establish connection to server.'),
                False,
                None
            )
        else:
            return res.caught_error, False, None
    else:
        # Check for API errors.
        if res.status_code == 200:
            return (None, False, None)
        elif res.status_code == 400:
            return (BadRequest(res.data), False, None)
        elif res.status_code == 401:
            # The first retry is #1. Therefor, retry_count < 2 will
            # result in a a single retry attempt.
            return (Unauthorized(res.data), retry_count < 2, None)
        elif res.status_code == 403:
            return (Forbidden(res.data), False, None)
        elif res.status_code == 404:
            return (NotFound(res.data), False, None)
        elif res.status_code == 409:
            return (Conflict(res.data), False, None)
        elif res.status_code == 429:
            if 'Retry-After' in res.headers:
                return (
                    TooManyRequests(res.data),
                    True,
                    int(res.headers['Retry-After'])
                )
            else:
                return (TooManyRequests(res.data), False, None)
        elif res.status_code == 500:
            return (InternalServerError(res.data), True, retry_count**2)
        elif res.status_code == 503:
            return (InternalServerError(res.data), True, retry_count**2)
        elif res.status_code == 504:
            return (InternalServerError(res.data), True, retry_count**2 + 9)
        else:
            return (UnknownError(res.data), False, None)
