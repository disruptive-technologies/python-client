class DTApiError(Exception):
    def __init__(self, message):
        # Create message from dictionary contents.
        formatted = 'Status Code {}.\nError: {}.\nHelp:  {}.'.format(
            message['code'],
            message['error'],
            message['help'],
        )

        # Call the base class constructor.
        super().__init__(formatted)


class BadRequest(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class Unauthenticated(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class Forbidden(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class NotFound(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class Conflict(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class TooManyRequests(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class InternalServerError(DTApiError):
    def __init__(self, message):
        super().__init__(message)


class ServerUnavailable(DTApiError):
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
