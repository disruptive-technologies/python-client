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
        assert p.id == res['name'].split('/')[-1]
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

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects',
        )

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

    def test_update(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtresponses.empty_project

        # Call the appropriate endpoint.
        dt.Project.update('project_id', 'new-name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=dt.base_url+'/projects/project_id',
            body={'displayName': 'new-name'},
        )

    def test_delete(self, request_mock):
        # Call the appropriate endpoint.
        dt.Project.delete('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.base_url+'/projects/project_id',
        )

    def test_list_members(self, request_mock):
        # Update the response data with list of member data.
        request_mock.json = dtresponses.members

        # Call the appropriate endpoint
        members = dt.Project.list_members('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/members',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for m in members:
            assert isinstance(m, dt.outputs.Member)

    def test_add_member(self, request_mock):
        # Update the response data with member data.
        res = dtresponses.user_member
        request_mock.json = res

        # Call the appropriate endpoint
        member = dt.Project.add_member(
            project_id='project_id',
            email='serviceaccount_email@domain.com',
            roles=['project.developer'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.base_url+'/projects/project_id/members',
            body={
                'roles': ['roles/project.developer'],
                'email': 'serviceaccount_email@domain.com',
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        assert isinstance(member, dt.outputs.Member)

    def test_get_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtresponses.user_member

        # Call the appropriate endpoint
        member = dt.Project.get_member(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/members/member_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        assert isinstance(member, dt.outputs.Member)

    def test_update_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtresponses.user_member

        # Call the appropriate endpoint
        member = dt.Project.update_member(
            project_id='project_id',
            member_id='member_id',
            roles=['project.developer'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=dt.base_url+'/projects/project_id/members/member_id',
            body={'roles': ['roles/project.developer']}
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        assert isinstance(member, dt.outputs.Member)

    def test_remove_member(self, request_mock):
        # Update the response with status code 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint
        response = dt.Project.remove_member(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.base_url+'/projects/project_id/members/member_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert response is None
