from __future__ import annotations

from typing import Any, Optional

import requests

import disruptive.outputs as dtoutputs
import disruptive.logging as dtlog


# ------------------------- Parent -------------------------
class DTApiError(Exception):
    """
    Represents errors raised from the REST API.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)

        # Log the error.
        dtlog.error(message)


# ------------------------- BatchErrors -------------------------
class BatchError(dtoutputs.OutputBase):
    """
    Parent class for errors in batch-style methods where one or several
    actions may fail in an otherwise successful request.

    """

    def __init__(self, error: Any) -> None:
        # Inherit from OutputBase parent.
        super().__init__(error)

        # Log the error.
        dtlog.error(error)


class TransferDeviceError(BatchError):
    """
    Represents errors that occur when a device can, for some reason, not
    be transferred from one project to another.

    Attributes
    ----------
    device_id : str
        Unique ID of the source device.
    project_id : str
        Unique ID of the source project.
    status_code : str
        A status code for the returned error. Is either
        "INVALID_ARGUMENT", "NOT_FOUND", or "INTERNAL_ERROR".
    message : str
        Described the cause of the error.

    """

    def __init__(self, error: dict) -> None:
        # Inherit from OutputBase parent.
        super().__init__(error)

        # Unpack error dictionary.
        self.device_id: str = error['device'].split('/')[-1]
        self.project_id: str = error['device'].split('/')[1]
        self.status_code: str = error['status']['code']
        self.message: str = error['status']['message']


class LabelUpdateError(BatchError):
    """
    Represents errors that occur when a label can, for some reason, not
    be updated for a device.

    Attributes
    ----------
    device_id : str
        Unique ID of the source device.
    project_id : str
        Unique ID of the source project.
    status_code : str
        A status code for the returned error. Is either
        "INVALID_ARGUMENT", "NOT_FOUND", or "INTERNAL_ERROR".
    message : str
        Described the cause of the error.

    """

    def __init__(self, error: dict) -> None:
        # Inherit from OutputBase parent.
        super().__init__(error)

        # Unpack error dictionary.
        self.device_id: str = error['device'].split('/')[-1]
        self.project_id: str = error['device'].split('/')[1]
        self.status_code: str = error['status']['code']
        self.message: str = error['status']['message']


# ------------------------- ServerError -------------------------
class ServerError(DTApiError):
    """
    Covers response errors in the 500 status code range.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class InternalServerError(ServerError):
    """
    The response contained a status code of 500.
    https://developer.d21s.com/docs/error-codes#500

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


# ------------------------- UsageError -------------------------
class UsageError(DTApiError):
    """
    Covers response errors in the 400 status code range in
    addition to problems caused by invalid parameter inputs.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class BadRequest(UsageError):
    """
    The response contained a status code of 400.
    https://developer.d21s.com/docs/error-codes#400

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class Unauthorized(UsageError):
    """
    The response contained a status code of 401.
    https://developer.d21s.com/docs/error-codes#401

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class Forbidden(UsageError):
    """
    The response contained a status code of 403.
    https://developer.d21s.com/docs/error-codes#403

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class NotFound(UsageError):
    """
    The response contained a status code of 404.
    https://developer.d21s.com/docs/error-codes#404

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class Conflict(UsageError):
    """
    The response contained a status code of 409.
    https://developer.d21s.com/docs/error-codes#409

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class TooManyRequests(UsageError):
    """
    The response contained a status code of 429.
    https://developer.d21s.com/docs/error-codes#429

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class FormatError(UsageError):
    """
    Some string formatting, usually a timestamp, is wrong.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class ConfigurationError(UsageError):
    """
    One or more :ref:`configuration parameters <configuration>` are invalid.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


# ------------------------- ConnectionError -------------------------
class ConnectionError(DTApiError):
    """
    Covers errors caused by unsuccessful connections from the client.
    These are mostly captured requests exceptions.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


class ReadTimeout(ConnectionError):
    """
    Could not connection to server in the alloted amount
    of time set by :ref:`request_timeout <config params>`.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


# ------------------------- UnknownError -------------------------
class UnknownError(DTApiError):
    """
    An unexpected exception has been raised.

    This is likely due to a bug in the package.
    Please report this to developer-support@disruptive-technologies.com.

    """

    def __init__(self, message: str | dict) -> None:
        super().__init__(message)


# ------------------------- error handling -------------------------
def parse_request_error(caught_error: Exception,
                        data: dict,
                        nth_attempt: int,
                        ) -> tuple:
    """
    Depending on the request error caught, choose a course of action.

    Parameters
    ----------
    caught_error : Exception
        Request error that has been caught.
    data : dict
        Data contained in the error-ridden request.
    nth_attempt : int
        Current request attempt.

    Returns
    -------
    error : Exception
        Exception to be raised.
    should_retry : bool
        If the request should be retried or not.
    nth_attempt : int
        Iterated attempt count.

    """

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


def parse_api_status_code(status_code: Optional[int],
                          data: dict,
                          headers: Any,
                          nth_attempt: int,
                          ) -> Any:
    """
    Depending on the status code, returns an exception, retry boolean
    and, incemented retry attempt.

    Parameters
    ----------
    status_code : int
        Status code returned by the API.
    data : dict
        Data in the response.
    headers : dict
        Headers in the response.
    nth_attempt : int
        Retry attempt count.

    Returns
    -------
    error : Exception
        The exception to be raised.
    should_retry : bool
        If the request should be retried.
    nth_attempt : int
        Incremented retry attempt count.

    """

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


def _raise_builtin(error: Any, message: str) -> Any:
    """
    Used to accompany raised builtin errors with a log message.

    Parameters
    ----------
    error : Exception
        Exception to be raised after logging.
    message : str
        Message to log.

    """

    # Log the error.
    dtlog.error(message)

    # Raise provided error.
    raise error(message)
