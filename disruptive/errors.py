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
            msg = 'Status Code {}.\nError: {}.\nHelp:  {}.'.format(
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


# Parses the status code, and returns (error, should_retry, retry_after)
def parse_error(status_code: int, headers: dict, retry_count: int):
    if status_code == 200:
        return (None, False, None)
    elif status_code == 400:
        return (BadRequest, False, None)
    elif status_code == 401:
        return (Unauthenticated, retry_count < 1, None)
    elif status_code == 403:
        return (Forbidden, False, None)
    elif status_code == 404:
        return (NotFound, False, None)
    elif status_code == 409:
        return (Conflict, False, None)
    elif status_code == 429:
        if 'Retry-After' in headers:
            return (TooManyRequests, True, int(headers['Retry-After']))
        else:
            return (TooManyRequests, False, None)
    elif status_code == 500:
        return (InternalServerError, True, retry_count**2)
    elif status_code == 503:
        return (InternalServerError, True, retry_count**2)
    elif status_code == 504:
        return (InternalServerError, True, retry_count**2 + 9)
