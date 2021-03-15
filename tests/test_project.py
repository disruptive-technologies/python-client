# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestProject():

    def test_unpack(self, request_mock):
        # Update the response data with device data.
        res = dtresponses.project
        request_mock.json = res

        # Call the appropriate endpoint.
        p = dt.Project.get('project_id')

        # Assert attributes unpacked correctly.
        assert p.display_name == res['displayName']
        assert p.organization_id == res['organization'].split('/')[-1]
        assert p.organization_display_name == res['organizationDisplayName']
        assert p.sensor_count == res['sensorCount']
        assert p.cloud_connector_count == res['cloudConnectorCount']

    def test_get(self, request_mock):
        # Update the response data with device data.
        request_mock.json = dtresponses.project

        # Call the appropriate endpoint.
        p = dt.Project.get('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id',
        )

        # Assert attributes in output Device object.
        assert isinstance(p, dt.Project)
