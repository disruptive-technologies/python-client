from __future__ import annotations

import time
import json
from typing import Optional, Any, Generator

import requests

import disruptive as dt
import disruptive.logging as dtlog
import disruptive.errors as dterrors


class DTRequest():

    def __init__(self, method: str, url: str, **kwargs: Any):
        # Set attributes from parameters.
        self.method = method
        self.url = url

        # Set default attributes, though many are updated in _unpack_kwargs().
        self.base_url = dt.base_url
        self.params: dict = dict()
        self.headers: dict = dict()
        self.body = None
        self.data = None
        self.request_timeout = dt.request_timeout
        self.request_attempts = dt.request_attempts

        # Unpack kwargs and set attributes thereafter.
        self._unpack_kwargs(**kwargs)

        # Check that provided arguments are valid.
        self._sanitize_arguments()

        # Construct full url from base and target endpoint.
        self.full_url = self.base_url + self.url

    def _unpack_kwargs(self, **kwargs: Any) -> None:
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

        # Check if request_attempts is overriden.
        if 'request_attempts' in kwargs:
            self.request_attempts = kwargs['request_attempts']

        # Check if base_url is overriden.
        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']

        # Add authorization header to request except when explicitly otherwise.
        if 'skip_auth' not in kwargs or kwargs['skip_auth'] is False:
            # If provided, override the package-wide auth with provided object.
            if 'auth' in kwargs:
                self.headers['Authorization'] = kwargs['auth'].get_token()
            # If not, use package-wide auth object.
            else:
                self.headers['Authorization'] = dt.default_auth.get_token()

    def _sanitize_arguments(self) -> None:
        # Check that request_timeout > 0.
        if self.request_timeout <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_timeout has value {}, but '
                'must be float greater than 0.'.format(self.request_timeout)
            )

        # Check that request_attempts > 0.
        if self.request_attempts <= 0:
            raise dterrors.ConfigurationError(
                'Configuration parameter request_attempts has value {}, but '
                'must be integer greater than 0.'.format(self.request_attempts)
            )

    def _request_wrapper(self,
                         method: str,
                         url: str,
                         params: dict,
                         headers: dict,
                         body: Optional[dict],
                         data: Optional[str],
                         timeout: int,
                         ) -> tuple[DTResponse, Any]:

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
                timeout=timeout,
                stream=False,
            )

            # Isolate the data of interest in the response.
            return DTResponse(res.json(), res.status_code, res.headers), None

        except requests.exceptions.RequestException as e:
            return DTResponse({}, None, {}), e
        except ValueError as e:
            # Requests' .json() fails when no json is returned (code 405).
            return DTResponse({}, res.status_code, res.headers), e

    def _send_request(self, nth_attempt: int = 1) -> dict:
        """
        Combines all the information and sends a request.

        Parameters
        ----------
        nth_attempt : int
            Request attempt count.

        Returns
        -------
        data : dict
            Data contained in the response.

        """

        # Log the request.
        dtlog.debug('Request [{}] to {}.'.format(
            self.method,
            self.base_url + self.url
        ))

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
        dtlog.debug('Response [{}].'.format(
            res.status_code
        ))

        # If _request_wrapper raised an exception, the request failed.
        if req_error is not None:
            error, should_retry, sleeptime = dterrors.parse_request_error(
                req_error, res.data, nth_attempt
            )
        else:
            # Parse the status_code and select an appropriate error.
            # If there is any hope at all that a retry might resolve the error,
            # should_retry will be True. (eg. a 401).
            error, should_retry, sleeptime = dterrors.parse_api_status_code(
                res.status_code, res.data, res.headers, nth_attempt
            )

        # Check if retry is required.
        if should_retry and nth_attempt < self.request_attempts:
            dtlog.error(error)
            dtlog.warning('Reconnecting in {}s.'.format(sleeptime))

            # Sleep if necessary.
            if sleeptime is not None:
                time.sleep(sleeptime)

            dtlog.info('Connection attempt {}/{}.'.format(
                nth_attempt+1,
                self.request_attempts,
            ))

            # Attempt the request again recursively, iterating counter.
            res.data = self._send_request(nth_attempt+1)

        else:
            # If set, raise the error chosen by dterrors.parse_error().
            if error is not None:
                raise error

        data: dict = res.data
        return data

    @classmethod
    def get(cls, url: str, **kwargs: Any) -> dict:
        req = cls('GET', url, **kwargs)
        response: dict = req._send_request()
        return response

    @classmethod
    def post(cls, url: str, **kwargs: Any) -> dict:
        req = cls('POST', url, **kwargs)
        response: dict = req._send_request()
        return response

    @classmethod
    def patch(cls, url: str, **kwargs: Any) -> dict:
        req = cls('PATCH', url, **kwargs)
        response: dict = req._send_request()
        return response

    @classmethod
    def delete(cls, url: str, **kwargs: Any) -> dict:
        req = cls('DELETE', url, **kwargs)
        response: dict = req._send_request()
        return response

    @classmethod
    def paginated_get(cls,
                      url: str,
                      pagination_key: str,
                      params: dict[str, str] = {},
                      **kwargs: Any,
                      ) -> list:
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

    @staticmethod
    def stream(url: str, **kwargs: Any) -> Generator:
        """
        Initialzed and returns a stream generator.

        Parameters
        ----------
        url : str
            API endpoint URL.

        """

        # Set ping constants.
        PING_INTERVAL = 10
        PING_JITTER = 2

        # Expand url with base_url.
        url = dt.base_url + url

        # Set error variable that if not None, raise it.
        error = None

        # Unpack kwargs.
        params = kwargs['params'] if 'params' in kwargs else {}
        headers = kwargs['headers'] if 'headers' in kwargs else {}
        if 'request_attempts' in kwargs:
            request_attempts = kwargs['request_attempts']
        else:
            request_attempts = dt.request_attempts

        # Add ping parameter to dictionary.
        params['ping_interval'] = str(PING_INTERVAL) + 's'

        # If provided, override package-wide auth with argument.
        if 'auth' in kwargs:
            headers['Authorization'] = kwargs['auth'].get_token()
        else:
            headers['Authorization'] = dt.default_auth.get_token()

        # Set up a simple catch-all retry policy.
        nth_attempt = 1
        while True:
            try:
                # Set up a stream connection.
                # Connection will timeout and reconnect if no single event
                # is received in an interval of ping_interval + ping_jitter.
                dtlog.info('Starting stream...')
                stream = requests.request(
                    method='GET',
                    url=url,
                    stream=True,
                    timeout=PING_INTERVAL + PING_JITTER,
                    params=params,
                    headers=headers,
                    json=None,
                    data=None,
                )

                # Iterate through the events as they come in (one per line).
                for line in stream.iter_lines():
                    # Decode the response payload and break on error.
                    payload = json.loads(line.decode('ascii'))
                    if 'result' in payload:
                        # Reset retry counter.
                        nth_attempt = 1

                        # Check for ping event.
                        event = payload['result']['event']
                        if event['eventType'] == 'ping':
                            dtlog.debug('Ping received.')
                            continue

                        # Yield event to generator.
                        yield event

                    elif 'error' in payload:
                        error, _, _ = dterrors.parse_api_status_code(
                            payload['error']['code'],
                            payload, None, 0
                        )
                        raise error

                    else:
                        raise dterrors.UnknownError(payload)

                # If the stream finished, but without an error, break the loop.
                dtlog.info('Stream ended without an error.')
                break

            except KeyboardInterrupt:
                break

            except requests.exceptions.RequestException as e:
                error, should_retry, sleeptime = dterrors.parse_request_error(
                    e, {}, nth_attempt)

                # Print the error and try again up to max_request_attempts.
                if nth_attempt < request_attempts and should_retry:
                    dtlog.error(error)
                    dtlog.warning('Reconnecting in {}s.'.format(sleeptime))

                    # Exponential backoff in sleep time.
                    time.sleep(sleeptime)

                    # Iterate attempt counter.
                    nth_attempt += 1
                    dtlog.info('Connection attempt {}/{}.'.format(
                        nth_attempt,
                        request_attempts,
                    ))

                else:
                    raise error


class DTResponse():

    def __init__(self,
                 data: dict,
                 status_code: Optional[int],
                 headers: Any,
                 ):

        self.data = data
        self.status_code = status_code
        self.headers = headers
