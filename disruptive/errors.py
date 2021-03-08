

class BadRequest(Exception):
    pass


class Unauthenticated(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass


class Conflict(Exception):
    pass


class TooManyRequests(Exception):
    pass


class InternalServerError(Exception):
    pass


class ServerUnavailable(Exception):
    pass


# Parses the status code, and returns (error, should_retry, retry_after)
def parse_error(status_code: int, headers: dict, retry_count: int):
    if status_code == 200:
        return (None, False, None)
    elif status_code == 400:
        return (BadRequest, False, None)
    elif status_code == 401:
        return (Unauthenticated, True, None)
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
