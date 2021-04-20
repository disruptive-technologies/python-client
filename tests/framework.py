# Project imports.
import disruptive as dt
from disruptive.authentication import Auth


class RequestsReponseMock():
    """
    A simple class used to imitate an requests.Response object.

    """

    def __init__(self, json, status_code, headers):
        self._json = json
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self._json


class RequestMock():

    def __init__(self, mocker):
        self._mocker = mocker

        self.json = {}
        self.status_code = 200
        self.headers = {}
        self.req_error = None

        self.request_patcher = self._mocker.patch(
            'requests.request',
            side_effect=self._patched_requests_request,
        )

        self.auth_expiration_patcher = self._mocker.patch.object(
            Auth,
            '_has_expired',
            return_value=False,
        )

        self.sleep_patcher = self._mocker.patch(
            'time.sleep',
        )

    def _patched_requests_request(self, **kwargs):
        return RequestsReponseMock(self.json, self.status_code, self.headers)

    def assert_request_count(self, n):
        if self.request_patcher.call_count != n:
            raise AssertionError

    def assert_requested(self,
                         method,
                         url,
                         params={},
                         headers={'Authorization': ''},
                         body=None,
                         data=None,
                         timeout=dt.request_timeout,
                         ):
        self.request_patcher.assert_called_with(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=body,
            data=data,
            timeout=timeout,
        )
