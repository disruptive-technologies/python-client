import pytest
import requests

import disruptive
import tests.api_responses as dtapiresponses
from disruptive.requests import DTRequest, DTResponse
from tests.framework import RequestsReponseMock


class TestRequests():

    def test_first_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Choose a response json to use.
        api_res = dtapiresponses.touch_count_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=[
                __patched_request(api_res, 200, {}),
                __patched_request({}, 500, {}),  # <- This should not run.
                __patched_request({}, 500, {}),  # <- This should not run.
            ],
        )
        # Call disruptive.Device.get_device() to trigger the request chain.
        device = disruptive.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed only 1 time.
        request_mock.assert_request_count(1)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_second_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Choose a response json to use.
        api_res = dtapiresponses.water_present_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=[
                __patched_request({}, 500, {}),
                __patched_request(api_res, 200, {}),
                __patched_request({}, 500, {}),  # <- This should not run.
            ],
        )
        # Call disruptive.Device.get_device() to trigger the request chain.
        device = disruptive.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed 2 times.
        request_mock.assert_request_count(2)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_third_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Choose a response json to use.
        api_res = dtapiresponses.touch_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=[
                __patched_request({}, 500, {}),
                __patched_request({}, 500, {}),
                __patched_request(api_res, 200, {}),
            ],
        )
        # Call disruptive.Device.get_device() to trigger the request chain.
        device = disruptive.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed 3 times.
        request_mock.assert_request_count(3)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_max_recursion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Choose a response json to use.
        api_res = dtapiresponses.temperature_sensor

        # As we want to test maxium depth, set n to package config variable.
        n = disruptive.request_attempts

        # Create in iterable side_effect for our mock.
        side_effects = [__patched_request({}, 500, {}) for i in range(n)]

        # Replace the last side_effect with a successful one.
        side_effects[-1] = __patched_request(api_res, 200, {})

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=side_effects,
        )

        # Call disruptive.Device.get_device() to trigger the request chain.
        device = disruptive.Device.get_device('project_id', 'device_id')

        # Verify recursive loop executed disruptive.request_attempts times.
        request_mock.assert_request_count(n)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_method_propagation(self, request_mock):
        # Assert GET method propagates correctly.
        DTRequest.get('/url')
        request_mock.assert_requested('GET', disruptive.base_url+'/url')

        # Assert POST method propagates correctly.
        DTRequest.post('/url')
        request_mock.assert_requested('POST', disruptive.base_url+'/url')

        # Assert PATCH method propagates correctly.
        DTRequest.patch('/url')
        request_mock.assert_requested('PATCH', disruptive.base_url+'/url')

        # Assert DELETE method propagates correctly.
        DTRequest.delete('/url')
        request_mock.assert_requested('DELETE', disruptive.base_url+'/url')

    def test_pagination_early_exit(self, request_mock):
        # Create a response we will update the page-token off.
        def __res(page_token: str):
            return {
                'nextPageToken': page_token,
                'events': [
                    history['events'][0],
                    history['events'][1],
                    history['events'][2],
                ]
            }

        # Fetch some event history data.
        history = dtapiresponses.event_history_each_type

        # Create a new request mock for request_mock object.
        # The default one is constant, which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'requests.request',
            side_effect=[
                RequestsReponseMock(__res('4'), 200, {}),
                RequestsReponseMock(__res('3'), 200, {}),
                RequestsReponseMock(__res(''), 200, {}),
                RequestsReponseMock(__res('2'), 200, {}),  # <- should not run
                RequestsReponseMock(__res('1'), 200, {}),  # <- should not run
            ],
        )

        # Call eventhistory method which should paginate 3 times.
        _ = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Verify it ran exactly 3 times.
        request_mock.assert_request_count(3)

        # The last request should have been made with page-token == '3'.
        url = disruptive.base_url
        url += '/projects/project_id/devices/device_id/events'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={'pageToken': '3'},
        )

    def test_pagination_max_depth(self, request_mock):
        # Create a response we will update the page-token off.
        def __res(page_token: str):
            return {
                'nextPageToken': page_token,
                'events': [
                    history['events'][0],
                    history['events'][1],
                    history['events'][2],
                ]
            }

        # Fetch some event history data.
        history = dtapiresponses.event_history_each_type

        # Create a new request mock for request_mock object.
        # The default one is constant, which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'requests.request',
            side_effect=[
                RequestsReponseMock(__res('4'), 200, {}),
                RequestsReponseMock(__res('3'), 200, {}),
                RequestsReponseMock(__res('2'), 200, {}),
                RequestsReponseMock(__res('1'), 200, {}),
                RequestsReponseMock(__res(''), 200, {}),
            ],
        )

        # Call eventhistory method which should paginate 5 times.
        _ = disruptive.EventHistory.list_events(
            device_id='device_id',
            project_id='project_id',
        )

        # Verify it ran exactly 5 times.
        request_mock.assert_request_count(5)

        # The last request should have been made with page-token == '1'.
        url = disruptive.base_url
        url += '/projects/project_id/devices/device_id/events'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={'pageToken': '1'},
        )

    def test_timeout_override(self, request_mock):
        # Set response to contain device data.
        request_mock.json = dtapiresponses.touch_sensor

        # Call Device.get_device(), overriden all defaults with kwargs.
        _ = disruptive.Device.get_device(
            device_id='device_id',
            request_timeout=99,
        )

        # Verify request were configured with new timeout.
        url = disruptive.base_url + '/projects/-/devices/device_id'
        request_mock.assert_requested(
            method='GET',
            url=url,
            timeout=99,
        )

    def test_request_attempts_override(self, request_mock):
        # Set response status code to force error with retry attemps.
        request_mock.status_code = 500

        # Catch expected error as retries are exhausted.
        with pytest.raises(disruptive.errors.InternalServerError):
            # Call Device.get_device() with overriden retry count.
            disruptive.Device.get_device(
                device_id='device_id',
                request_attempts=99,
            )

        # Verify it did in fact retry that many times.
        request_mock.assert_request_count(100)

    def test_request_attempts_invalid(self, request_mock):
        # Catch expected error as retries are exhausted.
        with pytest.raises(disruptive.errors.ConfigurationError):
            # Call Device.get_device() with overriden retry count.
            disruptive.Device.get_device(
                device_id='device_id',
                request_attempts=-1,
            )

    def test_request_timeout_invalid(self, request_mock):
        # Catch expected error as retries are exhausted.
        with pytest.raises(disruptive.errors.ConfigurationError):
            # Call Device.get_device() with overriden retry count.
            disruptive.Device.get_device(
                device_id='device_id',
                request_timeout=-1,
            )

    def test_request_caught_requests_connection_error(self, request_mock):
        # Re-mock requests.request with a new side_effect.
        request_mock.request_patcher = request_mock._mocker.patch(
            'requests.request',
            side_effect=requests.exceptions.ConnectionError,
        )

        # Catch the expected ConnectionError that should be raised.
        with pytest.raises(disruptive.errors.ConnectionError):
            # Call Device.get_device(), overriden all defaults with kwargs.
            _ = disruptive.Device.get_device(
                device_id='device_id',
                request_timeout=99,
            )

    def test_request_caught_generic_requests_error(self, request_mock):
        # Re-mock requests.request with a new side_effect.
        request_mock.request_patcher = request_mock._mocker.patch(
            'requests.request',
            side_effect=requests.exceptions.RequestException,
        )

        # Catch the expected ConnectionError that should be raised.
        with pytest.raises(requests.exceptions.RequestException):
            # Call Device.get_device(), overriden all defaults with kwargs.
            _ = disruptive.Device.get_device(
                device_id='device_id',
                request_timeout=99,
            )

    def test_request_caught_value_error(self, request_mock):
        # Re-mock requests.request with a new side_effect.
        request_mock.request_patcher = request_mock._mocker.patch(
            'requests.request',
            side_effect=requests.exceptions.RequestException,
        )

        # Catch the expected ConnectionError that should be raised.
        with pytest.raises(requests.exceptions.RequestException):
            # Call Device.get_device(), overriden all defaults with kwargs.
            _ = disruptive.Device.get_device(
                device_id='device_id',
                request_timeout=99,
            )
