import time
import json

import requests

import disruptive
import disruptive.log as log
import disruptive.errors as errors

# Constants.
MAX_RETRIES = 3
MAX_CONNECTION_RETRIES = 5
PING_INTERVAL = 10
PING_JITTER = 2


def get(endpoint: str,
        params={},
        headers={},
        timeout=None,
        auth=None
        ):
    return __send_request(
        "GET",
        endpoint,
        params,
        headers,
        timeout=timeout,
        auth=auth
    )


def post(endpoint: str,
         body: dict = None,
         data: str = None,
         headers: dict = {},
         authorize: bool = True,
         auth=None,
         ):
    return __send_request(
        "POST",
        endpoint,
        body=body,
        data=data,
        headers=headers,
        authorize=authorize,
        auth=auth,
    )


def patch(endpoint: str, body: dict, auth=None):
    return __send_request("PATCH", endpoint, body=body, auth=auth)


def delete(endpoint: str, auth=None):
    return __send_request("DELETE", endpoint, auth=auth)


def auto_paginated_list(
        endpoint: str,
        pagination_key: str,
        params: dict = {},
        page_size: int = 100,
        auth=None,
):
    results = []
    params['pageSize'] = page_size

    while True:
        response = __send_request("GET", endpoint, params=params, auth=auth)
        results += response[pagination_key]

        if len(response['nextPageToken']) > 0:
            params['pageToken'] = response['nextPageToken']
        else:
            break

    return results


def generator_list(
        endpoint: str,
        pagination_key: str,
        params: dict = {},
        page_size: int = 100,
        auth=None,
):
    params['pageSize'] = page_size

    while True:
        response = __send_request("GET", endpoint, params, auth=auth)

        yield response[pagination_key]

        if len(response['nextPageToken']) > 0:
            params['pageToken'] = response['nextPageToken']
        else:
            break


def __send_request(
        method: str,
        endpoint: str,
        params: dict = {},
        headers: dict = {},
        body: dict = None,
        data: str = None,
        retry_count: int = 0,
        timeout: int = 3,
        authorize: bool = True,
        auth=None,
):
    # Add headers to request
    if authorize:
        if auth is None:
            headers["Authorization"] = disruptive.auth.get_token()
        else:
            headers["Authorization"] = auth.get_token()
    for key in headers.keys():
        headers[key] = headers[key]

    # Send request.
    log.log('Request [{}] to {}.'.format(method, endpoint))
    response = requests.request(
        method=method,
        url=endpoint,
        params=params,
        headers=headers,
        json=body,
        data=data,
        timeout=timeout,
    )

    # Parse errors.
    # If there is any hope at all that a retry might resolve the error,
    # should_retry will be True. (eg. a 401).
    error, should_retry, retry_after = errors.parse_error(
        status_code=response.status_code,
        headers=response.headers,
        retry_count=retry_count,
    )

    # Check if retry is required
    if should_retry and retry_count >= MAX_RETRIES:

        log.log("Got error {}. Will retry up to {} more times".format(
            error,
            retry_count - MAX_RETRIES
        ))

        # Sleep if necessary.
        if retry_after is not None:
            time.sleep(retry_after)

        # Retry.
        __send_request(
            method=method,
            endpoint=endpoint,
            params=params,
            headers=headers,
            body=body,
            data=data,
            retry_count=retry_after + 1,
            authorize=authorize,
        )

    # Raise error if present.
    if error is not None:
        raise error(response.json())

    return response.json()


def stream(endpoint: str, params: dict):
    # Construct endpoint URL.
    url = disruptive.base_url + endpoint

    # Set streaming parameters and headers.
    params['ping_interval'] = '{}s'.format(PING_INTERVAL)
    headers = {
        'Authorization': disruptive.auth.get_token()
    }

    # Set up a simple catch-all retry policy.
    nth_retry = 0
    while nth_retry <= MAX_CONNECTION_RETRIES:
        try:
            # Set up a stream connection.
            # Connection will timeout and reconnect if no single event
            # is received in an interval of PING_INTERVAL + PING_JITTER.
            log.log('Starting stream...')
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
                    log.log('Got ping')
                    continue

                yield event

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(e)
            # Print the error and try again up to MAX_CONNECTION_RETRIES.
            if nth_retry < MAX_CONNECTION_RETRIES:
                log.log('Connection lost. Retry {}/{}.'.format(
                    nth_retry+1,
                    MAX_CONNECTION_RETRIES,
                ))

                # Exponential backoff in sleep time.
                time.sleep(2**nth_retry)
                nth_retry += 1
            else:
                break
