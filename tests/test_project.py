# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestProject():

    def test_unpack(self, request_mock):
        # Update the response data with project data.
        res = dtresponses.small_project
        request_mock.json = res

        # Call the appropriate endpoint.
        p = dt.Project.get_project('project_id')

        # Assert attributes unpacked correctly.
        assert p.id == res['name'].split('/')[-1]
        assert p.display_name == res['displayName']
        assert p.organization_id == res['organization'].split('/')[-1]
        assert p.organization_display_name == res['organizationDisplayName']
        assert p.sensor_count == res['sensorCount']
        assert p.cloud_connector_count == res['cloudConnectorCount']

    def test_get_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtresponses.small_project

        # Call the appropriate endpoint.
        p = dt.Project.get_project('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Project.
        assert isinstance(p, dt.Project)

    def test_list_projects(self, request_mock):
        # Update the response data with list of project data.
        request_mock.json = dtresponses.projects

        # Call the appropriate endpoint
        projects = dt.Project.list_projects()

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for p in projects:
            assert isinstance(p, dt.Project)

    def test_create_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtresponses.empty_project

        # Call the appropriate endpoint.
        p = dt.Project.create_project('org', 'name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.base_url+'/projects',
            body={'organization': 'organizations/org', 'displayName': 'name'},
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Project.
        assert isinstance(p, dt.Project)

    def test_update_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtresponses.empty_project

        # Call the appropriate endpoint.
        output = dt.Project.update_project('project_id', 'new-name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=dt.base_url+'/projects/project_id',
            body={'displayName': 'new-name'},
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert output is None

    def test_delete_project(self, request_mock):
        # Call the appropriate endpoint.
        output = dt.Project.delete_project('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.base_url+'/projects/project_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert output is None

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

        # Assert instances of Member in output list.
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

        # Assert output is instance of Member.
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

        # Assert output is instance of Member.
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

        # Assert output is instance of Member.
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

    def test_get_member_invite_url(self, request_mock):
        # Update the response with an email string.
        res = {'inviteUrl': 'some-email@domain.com'}
        request_mock.json = res

        # Call the appropriate endpoint
        response = dt.Project.get_member_invite_url(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/members/'
            + 'member_id:getInviteUrl',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output matches response content.
        assert response == res['inviteUrl']

    def test_list_permissions(self, request_mock):
        # Update the response with list of permissions.
        request_mock.json = dtresponses.project_permissions

        # Call the appropriate endpoint
        response = dt.Project.list_permissions(
            project_id='project_id',
        )

        # Assert output is of type list.
        assert type(response) == list

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/permissions'
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert only strings in output list.
        for permission in response:
            assert type(permission) == str
