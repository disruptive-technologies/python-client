# Project imports.
from disruptive.authentication import Auth
from disruptive.response import DTResponse


class RequestMock():

    def __init__(self, mocker):
        self._mocker = mocker

        self.json = {}
        self.status_code = 200
        self.headers = {}

        self.request_patcher = self._mocker.patch(
            'disruptive.requests.__send_request',
            side_effect=self._patched_request
        )

        self.auth_expiration_patcher = self._mocker.patch.object(
            Auth,
            'has_expired',
            return_value=False,
        )

    def _patched_request(self, **kwargs):
        return DTResponse(self.json, self.status_code, self.headers)

    def assert_request_count(self, n):
        if self.request_patcher.call_count != n:
            raise AssertionError
