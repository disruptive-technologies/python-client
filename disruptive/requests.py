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


class DTRequest():

    def __init__(self, method, url, **kwargs):
        # Set attributes from parameters.
        self.method = method
        self.url = url

        # Set default attributes, though many are updated in _unpack_kwargs().
        self.base_url = dt.api_url
        self.params = {}
        self.headers = {}
        self.body = None
        self.data = None
        self.request_timeout = dt.request_timeout
        self.request_retries = dt.request_retries
        self.log = dt.log

        # Unpack kwargs and set attributes thereafter.
        self._unpack_kwargs(**kwargs)

        # Check that provided arguments are valid.
        self._sanitize_arguments()

        # Construct full url from base and target endpoint.
        self.full_url = self.base_url + self.url

    def _unpack_kwargs(self, **kwargs):
        if 'params' in kwargs:
            self.params = kwargs['params']
        if 'headers' in kwargs:
            self.headers = kwargs['headers']
        if 'body' in kwargs:
            self.body = kwargs['body']
        if 'data' in kwargs:
            self.data = kwargs['data']

        # Check if request_timeout is overriden.
        if 'request_timeout' in kwargs:
            self.request_timeout = kwargs['request_timeout']

        # Check if request_retries is overriden.
        if 'request_retries' in kwargs:
            self.request_retries = kwargs['request_retries']

        # Check if base_url is overriden.
        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']

        # Check if log is overriden.
        if 'log' in kwargs:
            self.log = kwargs['log']

        # Add authorization header to request except when explicitly otherwise.
        if 'skip_auth' not in kwargs or kwargs['skip_auth'] is False:
            # If provided, override the package-wide auth with provided object.
            if 'auth' in kwargs:
                self.headers['Authorization'] = kwargs['auth'].get_token()
            # If not, use package-wide auth object.
            else:
                self.headers['Authorization'] = dt.default_auth.get_token()

    def _sanitize_arguments(self):
        # Check that request_timeout > 0.
        if self.request_timeout <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_timeout has value {}, but '
                'must be float greater than 0.'.format(self.request_timeout)
            )

        # Check that request_retries > 0.
        if self.request_retries <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_retries has value {}, but '
                'must be integer greater than 0.'.format(self.request_retries)
            )

    def _request_wrapper(self,
                         method: str,
                         url: str,
                         params: dict,
                         headers: dict,
                         body: Optional[dict],
                         data: Optional[str],
                         timeout: int,
                         ):
        # Attempt to send the request.
        try:
            # Use the requests package to send the request.
            res = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=body,
                data=data,
                timeout=timeout
            )

            # Isolate the data of interest in the response.
            return DTResponse(res.json(), res.status_code, res.headers), None

        except requests.exceptions.RequestException as e:
            return DTResponse({}, None, {}), e
        except ValueError as e:
            # Requests' .json() fails when no json is returned (code 405).
            return DTResponse({}, res.status_code, res.headers), e

    def _send_request(self, nth_attempt=1):
        # Log the request.
        dtlog.log('Request [{}] to {}.'.format(
            self.method,
            self.base_url + self.url
        ), override=self.log)

        res, req_error = self._request_wrapper(
            method=self.method,
            url=self.full_url,
            params=self.params,
            headers=self.headers,
            body=self.body,
            data=self.data,
            timeout=self.request_timeout,
        )

        # Log the response.
        dtlog.log('Response [{}].'.format(
            res.status_code
        ), override=self.log)

        # If _request_wrapper raised an exception, the request failed.
        if req_error is not None:
            error, should_retry, retry_after = self._parse_request_error(
                req_error, res.data, nth_attempt
            )
        else:
            # Parse the status_code and select an appropriate error.
            # If there is any hope at all that a retry might resolve the error,
            # should_retry will be True. (eg. a 401).
            error, should_retry, retry_after = self._parse_api_status_code(
                res.status_code, res.data, res.headers, nth_attempt
            )

        # Check if retry is required.
        if should_retry and nth_attempt < self.request_retries:

            dtlog.log("Got error {}. Will retry up to {} more times".format(
                error,
                dt.request_retries - nth_attempt,
            ), override=self.log)

            # Sleep if necessary.
            if retry_after is not None:
                time.sleep(retry_after)

            # Attempt the request again recursively, iterating counter.
            res.data = self._send_request(nth_attempt+1)

        else:
            # If set, raise the error chosen by dterrors.parse_error().
            if error is not None:
                raise error

        return res.data

    def _parse_request_error(self, caught_error, data, nth_attempt):
        # Read Timeouts should be attempted again.
        if isinstance(caught_error, requests.exceptions.ReadTimeout):
            return dterrors.ReadTimeout, True, nth_attempt**2

        # Connection errors should be attempted again.
        elif isinstance(caught_error, requests.exceptions.ConnectionError):
            return (
                ConnectionError('Failed to establish connection.'),
                True,
                nth_attempt**2,
            )
        else:
            # Uncategorized error has been raised.
            return dterrors.UnknownError(data), False, None

    def _parse_api_status_code(self, status_code, data, headers, nth_attempt):
        # Check for API errors.
        if status_code == 200:
            return None, False, None
        elif status_code == 400:
            return dterrors.BadRequest(data), False, None
        elif status_code == 401:
            # The first retry is #1. Therefor, retry_count < 2 will
            # result in a a single retry attempt.
            return dterrors.Unauthorized(data), nth_attempt < 2, None
        elif status_code == 403:
            return dterrors.Forbidden(data), False, None
        elif status_code == 404:
            return dterrors.NotFound(data), False, None
        elif status_code == 409:
            return dterrors.Conflict(data), False, None
        elif status_code == 429:
            if 'Retry-After' in headers:
                return (
                    dterrors.TooManyRequests(data),
                    True,
                    int(headers['Retry-After']),
                )
            else:
                return dterrors.TooManyRequests(data), False, None
        elif status_code == 500:
            return dterrors.InternalServerError(data), True, nth_attempt**2
        elif status_code == 503:
            return dterrors.InternalServerError(data), True, nth_attempt**2
        elif status_code == 504:
            return dterrors.InternalServerError(data), True, nth_attempt**2 + 9
        else:
            return dterrors.UnknownError(data), False, None

    @classmethod
    def get(cls, url, **kwargs):
        req = cls('GET', url, **kwargs)
        return req._send_request()

    @classmethod
    def post(cls, url, **kwargs):
        req = cls('POST', url, **kwargs)
        return req._send_request()

    @classmethod
    def patch(cls, url, **kwargs):
        req = cls('PATCH', url, **kwargs)
        return req._send_request()

    @classmethod
    def delete(cls, url, **kwargs):
        req = cls('DELETE', url, **kwargs)
        return req._send_request()

    @classmethod
    def paginated_get(cls,
                      url: str,
                      pagination_key: str,
                      params: dict[str, str] = {},
                      **kwargs
                      ):
        # Initialize output list.
        results = []

        # Loop until paging has finished.
        while True:
            response = cls.get(url, params=params, **kwargs)
            results += response[pagination_key]

            if len(response['nextPageToken']) > 0:
                params['pageToken'] = response['nextPageToken']
            else:
                break

        return results

    @classmethod
    def stream(cls, url: str, **kwargs):
        # Set ping constants.
        PING_INTERVAL = 10
        PING_JITTER = 2

        # Expand url with base_url.
        url = dt.api_url + url

        # Set error variable that if not None, raise it.
        error = None

        def stream_retry_logic(nth_attempt):
            # Print the error and try again up to max_request_retries.
            if nth_attempt < request_retries:
                dtlog.log('Connection lost. Retry {}/{}.'.format(
                    nth_attempt+1,
                    request_retries,
                ))

                # Exponential backoff in sleep time.
                time.sleep(2**nth_attempt)

                return nth_attempt + 1, None
            else:
                return nth_attempt, dterrors.ConnectionError(
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
        nth_attempt = 0
        while nth_attempt <= request_retries:
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
                    nth_attempt = 0

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
                nth_attempt, error = stream_retry_logic(nth_attempt)

            except requests.exceptions.ConnectionError:
                nth_attempt, error = stream_retry_logic(nth_attempt)


class DTResponse():

    def __init__(self, data, status_code, headers):
        self.data = data
        self.status_code = status_code
        self.headers = headers
