# Project imports.
import disruptive as dt
from disruptive.authentication import Unauthenticated


class RequestsReponseMock():
    """
    A simple class used to imitate an requests.Response object.

    """

    def __init__(self, json, status_code, headers, iter_data=[]):
        self._json = json
        self.status_code = status_code
        self.headers = headers
        self.iter_data = iter_data

    def json(self):
        return self._json

    def iter_lines(self):
        for d in self.iter_data:
            yield d


class RequestMock():

    def __init__(self, mocker):
        self._mocker = mocker

        self.json = {}
        self.status_code = 200
        self.headers = {}
        self.req_error = None
        self.iter_data = []

        self.request_patcher = self._mocker.patch(
            'requests.request',
            side_effect=self._patched_requests_request,
        )

        self.auth_expiration_patcher = self._mocker.patch.object(
            Unauthenticated,
            '_has_expired',
            return_value=False,
        )

        self.sleep_patcher = self._mocker.patch(
            'time.sleep',
        )

    def _patched_requests_request(self, **kwargs):
        return RequestsReponseMock(
            json=self.json,
            status_code=self.status_code,
            headers=self.headers,
            iter_data=self.iter_data,
        )

    def assert_request_count(self, n):
        if self.request_patcher.call_count != n:
            raise AssertionError

    def assert_requested(
        self,
        method,
        url,
        params={},
        headers={
            'Authorization': '',
            'User-Agent': f'DisruptivePythonAPI/{dt.__version__}'
        },
        body=None,
        data=None,
        timeout=dt.request_timeout,
        stream=False,
    ):
        self.request_patcher.assert_called_with(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=body,
            data=data,
            timeout=timeout,
            stream=stream,
        )
