import disruptive
import tests.api_responses as dtapiresponses


class TestProject():

    def test_repr(self, request_mock):
        # Update the response data with project data.
        res = dtapiresponses.small_project
        request_mock.json = res

        # Fetch a project.
        x = disruptive.Project.get_project(
            project_id='project_id',
        )

        # Evaluate __repr__ function and compare copy.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_unpack(self, request_mock):
        # Update the response data with project data.
        res = dtapiresponses.small_project
        request_mock.json = res

        # Call the appropriate endpoint.
        p = disruptive.Project.get_project('project_id')

        # Assert attributes unpacked correctly.
        assert p.project_id == res['name'].split('/')[-1]
        assert p.display_name == res['displayName']
        assert p.organization_id == res['organization'].split('/')[-1]
        assert p.organization_display_name == res['organizationDisplayName']
        assert p.sensor_count == res['sensorCount']
        assert p.cloud_connector_count == res['cloudConnectorCount']

    def test_get_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtapiresponses.small_project

        # Call the appropriate endpoint.
        p = disruptive.Project.get_project('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Project.
        assert isinstance(p, disruptive.Project)

    def test_list_projects(self, request_mock):
        # Update the response data with list of project data.
        request_mock.json = dtapiresponses.projects

        # Call the appropriate endpoint
        projects = disruptive.Project.list_projects()

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for p in projects:
            assert isinstance(p, disruptive.Project)

    def test_create_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtapiresponses.empty_project

        # Call the appropriate endpoint.
        p = disruptive.Project.create_project('org', 'name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=disruptive.base_url+'/projects',
            body={'organization': 'organizations/org', 'displayName': 'name'},
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Project.
        assert isinstance(p, disruptive.Project)

    def test_update_project(self, request_mock):
        # Update the response data with project data.
        request_mock.json = dtapiresponses.empty_project

        # Call the appropriate endpoint.
        output = disruptive.Project.update_project('project_id', 'new-name')

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=disruptive.base_url+'/projects/project_id',
            body={'displayName': 'new-name'},
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert output is None

    def test_delete_project(self, request_mock):
        # Call the appropriate endpoint.
        output = disruptive.Project.delete_project('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=disruptive.base_url+'/projects/project_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is None.
        assert output is None

    def test_list_members(self, request_mock):
        # Update the response data with list of member data.
        request_mock.json = dtapiresponses.members

        # Call the appropriate endpoint
        members = disruptive.Project.list_members('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/members',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Member in output list.
        for m in members:
            assert isinstance(m, disruptive.outputs.Member)

    def test_add_member(self, request_mock):
        # Update the response data with member data.
        res = dtapiresponses.user_member
        request_mock.json = res

        # Call the appropriate endpoint
        member = disruptive.Project.add_member(
            project_id='project_id',
            email='service_account_email@domain.com',
            roles=['project.developer'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=disruptive.base_url+'/projects/project_id/members',
            body={
                'roles': ['roles/project.developer'],
                'email': 'service_account_email@domain.com',
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Member.
        assert isinstance(member, disruptive.outputs.Member)

    def test_get_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtapiresponses.user_member

        # Call the appropriate endpoint
        member = disruptive.Project.get_member(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/members/member_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Member.
        assert isinstance(member, disruptive.outputs.Member)

    def test_update_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtapiresponses.user_member

        # Call the appropriate endpoint
        member = disruptive.Project.update_member(
            project_id='project_id',
            member_id='member_id',
            roles=['project.developer'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=disruptive.base_url+'/projects/project_id/members/member_id',
            body={'roles': ['roles/project.developer']}
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instance of Member.
        assert isinstance(member, disruptive.outputs.Member)

    def test_remove_member(self, request_mock):
        # Update the response with status code 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint
        response = disruptive.Project.remove_member(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=disruptive.base_url+'/projects/project_id/members/member_id',
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
        response = disruptive.Project.get_member_invite_url(
            project_id='project_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/members/'
            + 'member_id:getInviteUrl',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output matches response content.
        assert response == res['inviteUrl']

    def test_list_permissions(self, request_mock):
        # Update the response with list of permissions.
        request_mock.json = dtapiresponses.project_permissions

        # Call the appropriate endpoint
        response = disruptive.Project.list_permissions(
            project_id='project_id',
        )

        # Assert output is of type list.
        assert type(response) == list

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.base_url+'/projects/project_id/permissions'
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert only strings in output list.
        for permission in response:
            assert type(permission) == str
