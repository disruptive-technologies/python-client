import requests
from disruptive.responses import DTResponse


class DTApiError(Exception):
    """
    Represents errors raised from the REST API.

    """

    def __init__(self, message: dict):
        # If no message is provided, skip formatting.
        if len(message) == 0:
            msg = ''
        else:
            # Create message from dictionary contents.
            msg = 'Status Code {}\n\nError:\n{}\n\nHelp:\n{}'.format(
                message['code'],
                message['error'],
                message['help'],
            )

        # Call the base class constructor.
        super().__init__(msg)


class BadRequest(DTApiError):
    """
    The response contained a status code of 400.

    """

    def __init__(self, message):
        super().__init__(message)


class Unauthenticated(DTApiError):
    """
    The response contained a status code of 401.

    """

    def __init__(self, message):
        super().__init__(message)


class Forbidden(DTApiError):
    """
    The response contained a status code of 403.

    """

    def __init__(self, message):
        super().__init__(message)


class NotFound(DTApiError):
    """
    The response contained a status code of 404.

    """

    def __init__(self, message):
        super().__init__(message)


class Conflict(DTApiError):
    """
    The response contained a status code of 409.

    """

    def __init__(self, message):
        super().__init__(message)


class TooManyRequests(DTApiError):
    """
    The response contained a status code of 429.

    This entails that too many requests were made in
    too short of a timeframe.

    """

    def __init__(self, message):
        super().__init__(message)


class InternalServerError(DTApiError):
    """
    The response contained a status code of 500.

    """

    def __init__(self, message):
        super().__init__(message)


class ReadTimeout(Exception):
    """
    The server did not send any data in the allotted amount of time.

    """

    def __init__(self, message):
        super().__init__(message)


class ConnectionError(Exception):
    """
    Could not establish connection to the server.

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
    status_code : int
        Status code included in the request response.
    headers : dict
        Dictionary of headers included in the request response.
    retry_count : int
        Number of times the request has already been retried.

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
                ConnectionError('Failed to establish connection.'),
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
            return (Unauthenticated(res.data), retry_count < 1, None)
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
