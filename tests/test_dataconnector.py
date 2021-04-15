# Project imports.
import disruptive as dt
import tests.api_responses as dtapiresponses
import disruptive.dataconnector_configs.dataconnector_configs as dcon_configs


class TestDataconnector():

    def test_attributes(self, request_mock):
        # Update the response json with a mock dataconnector response.
        r = dtapiresponses.configured_dataconnector
        request_mock.json = r

        # Call the appropriate endpoint.
        d = dt.DataConnector.get_dataconnector('project_id', 'device_id')

        # Assert attributes unpacked correctly.
        assert d.dataconnector_id == r['name'].split('/')[-1]
        assert d.project_id == r['name'].split('/')[1]
        assert d.status == r['status']
        assert d.display_name == r['displayName']
        assert d.event_types == r['events']
        assert d.labels == r['labels']
        assert d.dataconnector_type == r['type']
        assert isinstance(d.config, dcon_configs.HttpPush)
        assert d.config.url == r['httpConfig']['url']
        assert d.config.signature_secret == r['httpConfig']['signatureSecret']
        assert d.config.headers == r['httpConfig']['headers']

    def test_unknown_config_type(self, request_mock):
        # Update the response json with a mock dataconnector of unknown type.
        r = dtapiresponses.configured_dataconnector
        r['type'] = 'unknown'
        request_mock.json = r

        # Call an endpoint to construct a dataconnector object.
        d = dt.DataConnector.get_dataconnector('project_id', 'device_id')

        # Assert config attribute is None.
        assert d.dataconnector_type == 'unknown'
        assert d.config is None

    def test_get_dataconnector(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = dtapiresponses.configured_dataconnector

        # Call the appropriate endpoint.
        d = dt.DataConnector.get_dataconnector('project_id', 'device_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        assert isinstance(d, dt.DataConnector)

    def test_list_dataconnectors(self, request_mock):
        # Update the response json with a mock dataconnector response.
        request_mock.json = dtapiresponses.paginated_dataconnectors_response

        # Call the appropriate endpoint.
        dataconnectors = dt.DataConnector.list_dataconnectors('project_id')

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        for d in dataconnectors:
            assert isinstance(d, dt.DataConnector)
