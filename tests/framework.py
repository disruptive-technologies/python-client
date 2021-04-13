# Project imports.
import disruptive as dt
import disruptive.responses as dtresponses
from disruptive.authentication import Auth


class RequestMock():

    def __init__(self, mocker):
        self._mocker = mocker

        self.json = {}
        self.status_code = 200
        self.headers = {}

        self.request_patcher = self._mocker.patch(
            'disruptive.requests._send_request',
            side_effect=self._patched_request
        )

        self.auth_expiration_patcher = self._mocker.patch.object(
            Auth,
            '_has_expired',
            return_value=False,
        )

        self.sleep_patcher = self._mocker.patch(
            'time.sleep',
        )

    def _patched_request(self, **kwargs):
        return dtresponses.DTResponse(
            self.json,
            self.status_code,
            self.headers
        )

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
            body=body,
            data=data,
            timeout=timeout,
        )
