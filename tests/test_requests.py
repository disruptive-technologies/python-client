# Project imports.
import disruptive as dt
import disruptive.responses as dtresponses
import tests.api_responses as dtapiresponses


class TestRequests():

    def test_first_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return dtresponses.DTResponse(json, status_code, headers)

        # Choose a response json to use.
        api_res = dtapiresponses.touch_count_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'disruptive.requests.__send_request',
            side_effect=[
                __patched_request(api_res, 200, {}),
                __patched_request({}, 500, {}),  # <- This should not run.
                __patched_request({}, 500, {}),  # <- This should not run.
            ],
        )
        # Call dt.Device.get_device() to trigger the request chain.
        device = dt.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed only 1 time.
        request_mock.assert_request_count(1)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_second_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return dtresponses.DTResponse(json, status_code, headers)

        # Choose a response json to use.
        api_res = dtapiresponses.water_present_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'disruptive.requests.__send_request',
            side_effect=[
                __patched_request({}, 500, {}),
                __patched_request(api_res, 200, {}),
                __patched_request({}, 500, {}),  # <- This should not run.
            ],
        )
        # Call dt.Device.get_device() to trigger the request chain.
        device = dt.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed 2 times.
        request_mock.assert_request_count(2)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_third_recusion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return dtresponses.DTResponse(json, status_code, headers)

        # Choose a response json to use.
        api_res = dtapiresponses.touch_sensor

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'disruptive.requests.__send_request',
            side_effect=[
                __patched_request({}, 500, {}),
                __patched_request({}, 500, {}),
                __patched_request(api_res, 200, {}),
            ],
        )
        # Call dt.Device.get_device() to trigger the request chain.
        device = dt.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed 3 times.
        request_mock.assert_request_count(3)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res

    def test_max_recursion_depth_success(self, request_mock):
        def __patched_request(json, status_code, headers):
            return dtresponses.DTResponse(json, status_code, headers)

        # Choose a response json to use.
        api_res = dtapiresponses.temperature_sensor

        # As we want to test maxium depth, set n to package config variable.
        n = dt.request_retries

        # Create in iterable side_effect for our mock.
        side_effects = [__patched_request({}, 500, {}) for i in range(n)]

        # Replace the last side_effect with a successful one.
        side_effects[-1] = __patched_request(api_res, 200, {})

        # Create a new request mock for request_mock object.
        # The default one is not recursive which we fix by
        # using an iterable side_effect which advances each call.
        request_mock.request_patcher = request_mock._mocker.patch(
            'disruptive.requests.__send_request',
            side_effect=side_effects,
        )
        # Call dt.Device.get_device() to trigger the request chain.
        device = dt.Device.get_device('project_id', 'device_id')

        # Verify that recursive loop executed dt.request_retries times.
        request_mock.assert_request_count(n)

        # Lastly, verify device object were built correctly.
        assert device._raw == api_res
