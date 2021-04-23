# Third-party imports.
import requests


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


def parse_request_error(caught_error, data, nth_attempt):
    # Read Timeouts should be attempted again.
    if isinstance(caught_error, requests.exceptions.ReadTimeout):
        return (
            ReadTimeout('Connection timed out.'),
            True,
            nth_attempt**2,
        )

    # Connection errors should be attempted again.
    elif isinstance(caught_error, requests.exceptions.ConnectionError):
        return (
            ConnectionError('Failed to establish connection.'),
            True,
            nth_attempt**2,
        )
    else:
        # Uncategorized error has been raised.
        return UnknownError(data), False, None


def parse_api_status_code(status_code, data, headers, nth_attempt):
    # Check for API errors.
    if status_code == 200:
        return None, False, None
    elif status_code == 400:
        return BadRequest(data), False, None
    elif status_code == 401:
        # The first retry is #1. Therefor, retry_count < 2 will
        # result in a a single retry attempt.
        return Unauthorized(data), nth_attempt < 2, None
    elif status_code == 403:
        return Forbidden(data), False, None
    elif status_code == 404:
        return NotFound(data), False, None
    elif status_code == 409:
        return Conflict(data), False, None
    elif status_code == 429:
        if 'Retry-After' in headers:
            return (
                TooManyRequests(data),
                True,
                int(headers['Retry-After']),
            )
        else:
            return TooManyRequests(data), False, None
    elif status_code == 500:
        return InternalServerError(data), True, nth_attempt**2
    elif status_code == 503:
        return InternalServerError(data), True, nth_attempt**2
    elif status_code == 504:
        return InternalServerError(data), True, nth_attempt**2 + 9
    else:
        return UnknownError(data), False, None
