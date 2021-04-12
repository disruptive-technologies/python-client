from __future__ import annotations

# Standard library imports.
import time
import json
from typing import Optional

# Third-party imports.
import requests

# Project imports
import disruptive as dt
import disruptive.log as dtlog
import disruptive.errors as dterrors
from disruptive.responses import DTResponse


def generic_request(method: str, url: str, **kwargs):
    """
    Generic request function used by most resource methods.

    Parameters
    ----------
    method : str
        Request method to use.
    url : str
        Target endpoint of request.
    params : dict, optional
        Parameters dictionary to include in request.
    headers : dict, optional
        Headers dictionary to include in request.
    body : dict, optional
        Body dictionary to include in request.
    data : str, optional
        Encoded data string to include in request.
    request_timeout : int, optional
        Number of seconds before request times out.
        Overwrites dt.request_timeout settings if provided.
    request_retries : int, optional
        Number of times to retry a request.
        Overwrites dt.request_retries settings if provided.
    auth : Auth, optional
        Object for authenticating the REST API.
        Overwrites dt.default_auth if provided.
    skip_auth : bool
        If provided with a value of True, excludes authentication header.

    Returns
    -------
    response : DTResponse
        An object representing the response and its content.

    """

    # Unpack all kwargs at once here for readability.
    params = kwargs['params'] if 'params' in kwargs else {}
    headers = kwargs['headers'] if 'headers' in kwargs else {}
    body = kwargs['body'] if 'body' in kwargs else None
    data = kwargs['data'] if 'data' in kwargs else None
    if 'request_timeout' in kwargs:
        request_timeout = kwargs['request_timeout']
        if request_timeout <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_timeout has value {}, but '
                'must be float greater than 0.'.format(request_timeout)
            )
    else:
        request_timeout = dt.request_timeout
    if 'request_retries' in kwargs:
        request_retries = kwargs['request_retries']
        if request_retries <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_retries has value {}, but '
                'must be integer greater than 0.'.format(request_retries)
            )
    else:
        request_retries = dt.request_retries

    # Check if the url is explicitly overriden by a user.
    if 'api_url' in kwargs:
        url = kwargs['api_url'] + url[len(dt.api_url):]
    elif 'emulator_url' in kwargs:
        url = kwargs['emulator_url'] + url[len(dt.emulator_url):]
    elif 'auth_url' in kwargs:
        url = kwargs['auth_url'] + url[len(dt.auth_url):]

    # Check if log is explicitly overriden by a user.
    if 'log' in kwargs:
        log_override = kwargs['log']
    else:
        log_override = dt.log

    # If this is the first recursive depth, retry counter is set to 1.
    # Adding it to kwargs like this is maybe a little weird, but is done as
    # the function is called recursively, which may results
    # in "double argument" problems if taken in as an argument.
    # Also, it works just fine.
    if 'retry_count' not in kwargs:
        kwargs['retry_count'] = 1

    # Add authorization header to request except when explicitly told not to.
    if 'skip_auth' not in kwargs or kwargs['skip_auth'] is False:
        # If provided, override the package-wide auth with provided object.
        if 'auth' in kwargs:
            headers['Authorization'] = kwargs['auth'].get_token()
        # If not, use package-wide auth object.
        else:
            headers['Authorization'] = dt.default_auth.get_token()

    # Send request.
    dtlog.log('Request [{}] to {}.'.format(method, url), override=log_override)
    response = __send_request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        body=body,
        data=data,
        timeout=request_timeout,
    )
    dtlog.log('Response [{}].'.format(
        response.status_code
    ), override=log_override)

    # Parse errors.
    # If there is any hope at all that a retry might resolve the error,
    # should_retry will be True. (eg. a 401).
    error, should_retry, retry_after = dterrors.parse_error(
        response,
        retry_count=kwargs['retry_count'],
    )

    # Check if retry is required.
    if should_retry and kwargs['retry_count'] < request_retries:

        dtlog.log("Got error {}. Will retry up to {} more times".format(
            error,
            dt.request_retries - kwargs['retry_count'],
        ), override=log_override)

        # Sleep if necessary.
        if retry_after is not None:
            time.sleep(retry_after)

        # Retry.
        kwargs['retry_count'] += 1
        generic_request(
            method=method,
            url=url,
            **kwargs,
        )

    # Raise error if present.
    if error is not None:
        raise error

    return response.data


def auto_paginated_list(url: str,
                        pagination_key: str,
                        params: dict[str, str] = {},
                        **kwargs,
                        ):
    # Initialize output list.
    results = []

    # Unpack all kwargs at once here for readability.
    if 'page_size' in kwargs:
        params['pageSize'] = kwargs['page_size']

    # Loop until paging has finished.
    while True:
        response = generic_request("GET", url, params=params, **kwargs)
        results += response[pagination_key]

        if len(response['nextPageToken']) > 0:
            params['pageToken'] = response['nextPageToken']
        else:
            break

    return results


def stream(url: str, **kwargs):
    # Set ping constants.
    PING_INTERVAL = 10
    PING_JITTER = 2

    # Set error variable that if not None, raise it.
    error = None

    def stream_retry_logic(nth_retry):
        # Print the error and try again up to max_request_retries.
        if nth_retry < request_retries:
            dtlog.log('Connection lost. Retry {}/{}.'.format(
                nth_retry+1,
                request_retries,
            ))

            # Exponential backoff in sleep time.
            time.sleep(2**nth_retry)

            return nth_retry + 1, None
        else:
            return nth_retry, dterrors.ConnectionError(
                'Stream retry attempts has been exhausted.'
            )

    # Unpack kwargs.
    params = kwargs['params'] if 'params' in kwargs else {}
    headers = kwargs['headers'] if 'headers' in kwargs else {}
    if 'request_retries' in kwargs:
        request_retries = kwargs['request_retries']
    else:
        request_retries = dt.request_retries

    # Add ping parameter to dictionary.
    params['ping_interval'] = str(PING_INTERVAL) + 's'

    # If provided, override package-wide auth with argument.
    if 'auth' in kwargs:
        headers['Authorization'] = kwargs['auth'].get_token()
    else:
        headers['Authorization'] = dt.default_auth.get_token()

    # Set up a simple catch-all retry policy.
    nth_retry = 0
    while nth_retry <= request_retries:
        # Check if error is set.
        if error is not None:
            raise error

        try:
            # Set up a stream connection.
            # Connection will timeout and reconnect if no single event
            # is received in an interval of ping_interval + ping_jitter.
            dtlog.log('Starting stream...')
            stream = requests.get(
                url=url,
                stream=True,
                timeout=PING_INTERVAL + PING_JITTER,
                params=params,
                headers=headers,
            )

            # Iterate through the events as they come in (one per line).
            for line in stream.iter_lines():
                # Decode the response payload and break on error.
                payload = json.loads(line.decode('ascii'))
                if 'result' not in payload:
                    break

                # Reset retry counter.
                nth_retry = 0

                # Check for ping event.
                event = payload['result']['event']
                if event['eventType'] == 'ping':
                    dtlog.log('Ping received.')
                    continue

                # Yield event to generator.
                yield event

        except KeyboardInterrupt:
            break

        except requests.exceptions.ReadTimeout:
            nth_retry, error = stream_retry_logic(nth_retry)

        except requests.exceptions.ConnectionError:
            nth_retry, error = stream_retry_logic(nth_retry)


def __send_request(method: str,
                   url: str,
                   params: dict,
                   headers: dict,
                   body: Optional[dict],
                   data: Optional[str],
                   timeout: int,
                   ):
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=body,
            data=data,
            timeout=timeout
        )

        res = DTResponse(
            response.json(),
            response.status_code,
            dict(response.headers),
        )
    except requests.exceptions.RequestException as e:
        res = DTResponse({}, None, {}, caught_error=e)
    except ValueError:
        # Requests' .json() method fails when no json is returned (code 405).
        res = DTResponse({}, response.status_code, dict(response.headers))

    return res
