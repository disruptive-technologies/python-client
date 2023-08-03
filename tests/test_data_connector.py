from unittest.mock import patch

import disruptive
import tests.api_responses as dtapiresponses


class TestDataconnector():

    def test_repr(self, request_mock):
        # Update the response data with Data Connector data.
        res = dtapiresponses.configured_data_connector
        request_mock.json = res

        # Fetch a Data Connector..
        x = disruptive.DataConnector.get_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Evaluate __repr__ function and compare copy.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_attributes(self, request_mock):
        # Update the response json with a mock Data Connector response.
        r = dtapiresponses.configured_data_connector
        request_mock.json = r

        # Call the appropriate endpoint.
        d = disruptive.DataConnector.get_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Assert attributes unpacked correctly.
        assert d.data_connector_id == r['name'].split('/')[-1]
        assert d.project_id == r['name'].split('/')[1]
        assert d.status == r['status']
        assert d.display_name == r['displayName']
        assert d.event_types == r['events']
        assert d.labels == r['labels']
        assert d.data_connector_type == r['type']
        assert isinstance(d.config, disruptive.DataConnector.HttpPushConfig)
        assert d.config.url == r['httpConfig']['url']
        assert d.config.signature_secret == r['httpConfig']['signatureSecret']
        assert d.config.headers == r['httpConfig']['headers']

    def test_unknown_config_type(self, request_mock):
        # Update the response json with a mock Data Connector of unknown type.
        r = dtapiresponses.unknown_data_connector
        request_mock.json = r

        # Call an endpoint to construct a Data Connector object.
        d = disruptive.DataConnector.get_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Assert config attribute is None.
        assert d.data_connector_type == 'unknown'
        assert d.config is None

    def test_get_data_connector(self, request_mock):
        # Update the response json with a mock Data Connector response.
        request_mock.json = dtapiresponses.configured_data_connector

        # Call the appropriate endpoint.
        d = disruptive.DataConnector.get_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url
        url += '/projects/project_id/dataconnectors/data_connector_id'
        request_mock.assert_requested(
            method='GET',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output instance.
        assert isinstance(d, disruptive.DataConnector)

    def test_list_data_connectors(self, request_mock):
        # Update the response json with a mock Data Connector response.
        request_mock.json = dtapiresponses.paginated_data_connectors_response

        # Call the appropriate endpoint.
        data_connectors = disruptive.DataConnector.list_data_connectors(
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url+'/projects/project_id/dataconnectors'
        request_mock.assert_requested(
            method='GET',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output as list of instances.
        assert isinstance(data_connectors, list)
        for d in data_connectors:
            assert isinstance(d, disruptive.DataConnector)

    def test_create_data_connector(self, request_mock):
        # Update the response json with a mock dataconnector response.
        res = dtapiresponses.configured_data_connector
        request_mock.json = res

        # Call DataConnector.configured_data_connector().
        d = disruptive.DataConnector.create_data_connector(
            project_id='c0md3pm0p7bet3vico8g',
            display_name='my-new-dcon',
            labels=['name', 'custom-label-01', 'custom_label-02'],
            config=disruptive.DataConnector.HttpPushConfig(
                url='https://584087e0a1fa.eu.ngrok.io/api/endpoint',
                signature_secret='some-very-good-secret',
                headers={
                    'another-header': 'header-contents',
                    'some-header': 'abc123',
                }
            )
        )

        # Verify expected outgoing parameters in request.
        # Especially the body is important here.
        url = disruptive.base_url
        url += '/projects/c0md3pm0p7bet3vico8g/dataconnectors'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'status': 'ACTIVE',
                'events': [],
                'labels': ['name', 'custom-label-01', 'custom_label-02'],
                'displayName': 'my-new-dcon',
                'type': 'HTTP_PUSH',
                'httpConfig': {
                    'url': 'https://584087e0a1fa.eu.ngrok.io/api/endpoint',
                    'signatureSecret': 'some-very-good-secret',
                    'headers': {
                        'another-header': 'header-contents',
                        'some-header': 'abc123'}
                }
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of DataConnector.
        assert isinstance(d, disruptive.DataConnector)

    def test_create_data_connector_http_push_config(self, request_mock):
        """
        Test that the creation of a Data Connector using HttpPush config
        will set the expected type and request body.

        """

        # Mock the DataConnector constructor to do nothing as
        # the response is not relevant to this test.
        with patch('disruptive.DataConnector.__init__') as init_mock:
            # Do nothing and return None.
            init_mock.return_value = None

            # Call DataConnector.create_data_connector for type HTTP_PUSH.
            disruptive.DataConnector.create_data_connector(
                project_id='project_id',
                config=disruptive.DataConnector.HttpPushConfig(
                    url='some-url',
                    signature_secret='some-secret',
                    headers={'name': 'value'},
                ),
            )

        # Verify expected outgoing parameters in request.
        # Especially the body is important here.
        url = disruptive.base_url+'/projects/project_id/dataconnectors'
        request_mock.assert_requested(
            method='POST',
            url=url,
            body={
                'status': 'ACTIVE',
                'events': [],
                'labels': [],
                'type': 'HTTP_PUSH',
                'httpConfig': {
                    'url': 'some-url',
                    'signatureSecret': 'some-secret',
                    'headers': {
                        'name': 'value',
                    }
                }
            }
        )

    def test_update_data_connector(self, request_mock):
        # Update the response json with a mock Data Connector response.
        res = dtapiresponses.configured_data_connector
        request_mock.json = res

        # Call DataConnector.configured_data_connector().
        d = disruptive.DataConnector.update_data_connector(
            data_connector_id='c16pegipidie7lltrefg',
            project_id='c0md3pm0p7bet3vico8g',
            display_name='my-new-dcon',
            labels=['name', 'custom-label-01', 'custom_label-02'],
            status='ACTIVE',
            event_types=['touch', 'temperature', 'objectPresent'],
            config=disruptive.DataConnector.HttpPushConfig(
                url='https://584087e0a1fa.eu.ngrok.io/api/endpoint',
                signature_secret='some-very-good-secret',
                headers={
                    'another-header': 'header-contents',
                    'some-header': 'abc123',
                }
            )
        )

        # Verify expected outgoing parameters in request.
        # Especially the body is important here.
        url = disruptive.base_url
        url += '/projects/c0md3pm0p7bet3vico8g'
        url += '/dataconnectors/c16pegipidie7lltrefg'
        request_mock.assert_requested(
            method='PATCH',
            url=url,
            body={
                'displayName': 'my-new-dcon',
                'status': 'ACTIVE',
                'events': ['touch', 'temperature', 'objectPresent'],
                'labels': ['name', 'custom-label-01', 'custom_label-02'],
                'httpConfig': {
                    'url': 'https://584087e0a1fa.eu.ngrok.io/api/endpoint',
                    'signatureSecret': 'some-very-good-secret',
                    'headers': {
                        'another-header': 'header-contents',
                        'some-header': 'abc123',
                    }
                }
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of DataConnector.
        assert isinstance(d, disruptive.DataConnector)

    def test_update_data_connector_change_nothing(self, request_mock):
        """
        Verify that if not provided, optional parameters should not
        be included in the request body. This is important as we do
        not want the API to change anything not provided.

        """

        # Mock the DataConnector constructor to do nothing as
        # the response is not relevant to this test.
        with patch('disruptive.DataConnector.__init__') as init_mock:
            # Do nothing and return None.
            init_mock.return_value = None

            # Call DataConnector.configured_data_connector() with only
            # required parameters, basically asking the API to change nothing.
            disruptive.DataConnector.update_data_connector(
                data_connector_id='data_connector_id',
                project_id='project_id',
            )

        # Verify that all optional parameters are not included in the body.
        url = disruptive.base_url
        url += '/projects/project_id/dataconnectors/data_connector_id'
        request_mock.assert_requested(
            method='PATCH',
            url=url,
            body={},
        )

    def test_delete_data_connector(self, request_mock):
        # Call the DataConnector.delete_data_connector() method.
        d = disruptive.DataConnector.delete_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url
        url += '/projects/project_id/dataconnectors/data_connector_id'
        request_mock.assert_requested(
            method='DELETE',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert that method returns nothing.
        assert d is None

    def test_get_metrics(self, request_mock):
        # Update the response json with a mock metric response.
        request_mock.json = dtapiresponses.metrics

        # Call DataConnector.get_metrics.
        m = disruptive.DataConnector.get_metrics(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url
        url += '/projects/project_id/dataconnectors/data_connector_id:metrics'
        request_mock.assert_requested(
            method='GET',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Metric.
        assert isinstance(m, disruptive.resources.data_connector.Metric)

    def test_sync_data_connector(self, request_mock):
        # Call DataConnector.sync_data_connector.
        m = disruptive.DataConnector.sync_data_connector(
            data_connector_id='data_connector_id',
            project_id='project_id',
        )

        # Verify expected outgoing parameters in request.
        url = disruptive.base_url
        url += '/projects/project_id/dataconnectors/data_connector_id:sync'
        request_mock.assert_requested(
            method='POST',
            url=url,
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert m is None

    def test_http_push_config_inbound(self, request_mock):
        """
        Test that fetching a Data Connector with type `HTTP_PUSH` will
        result in a config attribute of instance HttpPush.

        """
        # Update the response json with a mock Data Connector response.
        r = dtapiresponses.configured_data_connector
        request_mock.json = r

        # Call the appropriate endpoint.
        d = disruptive.DataConnector.get_data_connector(
            data_connector_id='c16eegpdidie7lltpefg',
            project_id='c0md3mm0c7pet3vico8g',
        )

        # Assert type and config instance.
        assert d.data_connector_type == 'HTTP_PUSH'
        assert isinstance(d.config, disruptive.DataConnector.HttpPushConfig)

        # Assert HttpPush attributes are set properly.
        assert d.config.url == r['httpConfig']['url']
        assert d.config.signature_secret == r['httpConfig']['signatureSecret']
        assert d.config.headers == r['httpConfig']['headers']

    def test_http_push_config_outbound(self):
        """
        Test that creating a Data Connector with an HttpPush object will
        result in the correct type- and request body construction.

        """

        # Construct a HttpPush object.
        config = disruptive.DataConnector.HttpPushConfig(
            url='some-url',
            signature_secret='some-secret',
            headers={
                'h1': 'v1',
                'h2': 'v2',
            },
        )

        # Verify type attribute is correct.
        assert config.data_connector_type == 'HTTP_PUSH'

        # Test that _to_dict() method returns expected format.
        expected = {
            'url': 'some-url',
            'signatureSecret': 'some-secret',
            'headers': {
                'h1': 'v1',
                'h2': 'v2',
            }
        }
        key, value = config._to_dict()
        assert key == 'httpConfig'
        assert value == expected
