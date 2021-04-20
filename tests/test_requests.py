# Project imports.
import disruptive
import tests.api_responses as dtapiresponses
from disruptive.requests import DTRequest, DTResponse


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
        n = disruptive.request_retries

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

        # Verify that recursive loop executed disruptive.request_retries times.
        request_mock.assert_request_count(n)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_method_propagation(self, request_mock):
        # Assert GET method propagates correctly.
        DTRequest.get('/url')
        request_mock.assert_requested('GET', disruptive.api_url+'/url')

        # Assert POST method propagates correctly.
        DTRequest.post('/url')
        request_mock.assert_requested('POST', disruptive.api_url+'/url')

        # Assert PATCH method propagates correctly.
        DTRequest.patch('/url')
        request_mock.assert_requested('PATCH', disruptive.api_url+'/url')

        # Assert DELETE method propagates correctly.
        DTRequest.delete('/url')
        request_mock.assert_requested('DELETE', disruptive.api_url+'/url')

    def test_pagination_early_exit(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Create a response we will update the page-token off.
        def __res(page_token: str):
            return {
                'nextPageToken': page_token,
                'events': [
                    dtapiresponses.event_history_each_type['events'][0],
                    dtapiresponses.event_history_each_type['events'][1],
                    dtapiresponses.event_history_each_type['events'][2],
                ]
            }

        # Create a new request mock for request_mock object.
        # The default one is constant, which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=[
                __patched_request(__res('4'), 200, {}),
                __patched_request(__res('3'), 200, {}),
                __patched_request(__res(''), 200, {}),
                __patched_request(__res('2'), 200, {}),  # <- should not run
                __patched_request(__res('1'), 200, {}),  # <- should not run
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
        url = disruptive.api_url
        url += '/projects/project_id/devices/device_id/events'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={'pageToken': '3'},
        )

    def test_pagination_max_depth(self, request_mock):
        def __patched_request(json, status_code, headers):
            return DTResponse(json, status_code, headers), None

        # Create a response we will update the page-token off.
        def __res(page_token: str):
            return {
                'nextPageToken': page_token,
                'events': [
                    dtapiresponses.event_history_each_type['events'][0],
                    dtapiresponses.event_history_each_type['events'][1],
                    dtapiresponses.event_history_each_type['events'][2],
                ]
            }

        # Create a new request mock for request_mock object.
        # The default one is constant, which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch.object(
            DTRequest,
            '_request_wrapper',
            side_effect=[
                __patched_request(__res('4'), 200, {}),
                __patched_request(__res('3'), 200, {}),
                __patched_request(__res('2'), 200, {}),
                __patched_request(__res('1'), 200, {}),
                __patched_request(__res(''), 200, {}),
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
        url = disruptive.api_url
        url += '/projects/project_id/devices/device_id/events'
        request_mock.assert_requested(
            method='GET',
            url=url,
            params={'pageToken': '1'},
        )
