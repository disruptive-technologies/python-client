# Project imports.
import disruptive as dt

# Test imports.
import tests.mock_responses as mock_responses


class TestDataconnector():

    def test_attributes(self, request_mock):
        # Update the response json with a mock dataconnector response.
        res = mock_responses.dataconnectors['single']
        request_mock.json = res

        # Call the appropriate endpoint.
        d = dt.Dataconnector.get('project_id', 'device_id')

        # Assert attributes unpacked correctly.
        assert d.id == res['name'].split('/')[-1]
        assert d.type == res['type']
        assert d.status == res['status']
        assert d.display_name == res['displayName']

    def test_get(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = mock_responses.dataconnectors['single']

        # Call the appropriate endpoint.
        d = dt.Dataconnector.get('project_id', 'device_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        assert isinstance(d, dt.Dataconnector)

    def test_list(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = mock_responses.dataconnectors['list']

        # Call the appropriate endpoint.
        dataconnectors = dt.Dataconnector.list('project_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        for d in dataconnectors:
            assert isinstance(d, dt.Dataconnector)
