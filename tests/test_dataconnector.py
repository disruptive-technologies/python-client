# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestDataconnector():

    def test_attributes(self, request_mock):
        # Update the response json with a mock dataconnector response.
        res = dtresponses.configured_dataconnector
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.DataConnector.get('project_id', 'device_id')

        # Assert attributes unpacked correctly.
        assert d.dataconnector_id == res['name'].split('/')[-1]
        assert d.type == res['type']
        assert d.status == res['status']
        assert d.display_name == res['displayName']

    def test_get(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = dtresponses.configured_dataconnector

        # Call the appropriate endpoint.
        d = dt.DataConnector.get('project_id', 'device_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        assert isinstance(d, dt.DataConnector)

    def test_listing(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = dtresponses.paginated_dataconnectors_response

        # Call the appropriate endpoint.
        dataconnectors = dt.DataConnector.listing('project_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        for d in dataconnectors:
            assert isinstance(d, dt.DataConnector)
