# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestProject():

    def test_unpack(self, request_mock):
        # Update the response data with project data.
        res = dtresponses.small_project
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
        # Update the response data with project data.
        request_mock.json = dtresponses.small_project

        # Call the appropriate endpoint.
        p = dt.Project.get('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id',
        )

        # Assert attributes in output Device object.
        assert isinstance(p, dt.Project)

    def test_list(self, request_mock):
        # Update the response data with list of project data.
        request_mock.json = dtresponses.projects

        # Call the appropriate endpoint
        projects = dt.Project.list()

        # Assert instances of Project in output list.
        for p in projects:
            assert isinstance(p, dt.Project)

    def test_create(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtresponses.empty_project

        # Call the appropriate endpoint.
        p = dt.Project.create('org', 'name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.base_url+'/projects',
            body={'organization': 'organizations/org', 'displayName': 'name'},
        )

        # Assert attributes in output Device object.
        assert isinstance(p, dt.Project)
