# Project imports.
import disruptive as dt
import tests.api_responses as dtapiresponses


class TestOrganization():

    def test_unpack(self, request_mock):
        # Update the response data with organization data.
        res = dtapiresponses.organization
        request_mock.json = res

        # Call the appropriate endpoint.
        o = dt.Organization.get_organization('organization_id')

        # Assert attributes unpacked correctly.
        assert o.id == res['name'].split('/')[-1]
        assert o.display_name == res['displayName']

    def test_get_organization(self, request_mock):
        # Update the response data with organization data.
        request_mock.json = dtapiresponses.organization

        # Call the appropriate endpoint.
        o = dt.Organization.get_organization('organization_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations/organization_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Organization object.
        assert isinstance(o, dt.Organization)

    def test_list_organizations(self, request_mock):
        # Update the response data with list of organization data.
        request_mock.json = dtapiresponses.organizations

        # Call the appropriate endpoint
        orgs = dt.Organization.list_organizations()

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Organization in output list.
        for o in orgs:
            assert isinstance(o, dt.Organization)

    def test_list_members(self, request_mock):
        # Update the response data with list of member data.
        request_mock.json = dtapiresponses.members

        # Call the appropriate endpoint
        members = dt.Organization.list_members('org_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations/org_id/members',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Member in output list.
        for m in members:
            assert isinstance(m, dt.outputs.Member)

    def test_add_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtapiresponses.serviceaccount_member

        # Call the appropriate endpoint
        member = dt.Organization.add_member(
            organization_id='org_id',
            email='serviceaccount_email@domain.com',
            roles=['organization.admin'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.api_url+'/organizations/org_id/members',
            body={
                'roles': ['roles/organization.admin'],
                'email': 'serviceaccount_email@domain.com',
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instances of Member.
        assert isinstance(member, dt.outputs.Member)

    def test_get_member(self, request_mock):
        # Update the response data with member data.
        request_mock.json = dtapiresponses.serviceaccount_member

        # Call the appropriate endpoint
        member = dt.Organization.get_member(
            organization_id='org_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations/org_id/members/member_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output is instances of Member.
        assert isinstance(member, dt.outputs.Member)

    def test_remove_member(self, request_mock):
        # Update the response with status code 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint
        response = dt.Organization.remove_member(
            organization_id='org_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.api_url+'/organizations/org_id/members/member_id',
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
        response = dt.Organization.get_member_invite_url(
            organization_id='org_id',
            member_id='member_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations/org_id/members/'
            + 'member_id:getInviteUrl',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert output matches response content.
        assert response == res['inviteUrl']

    def test_list_permissions(self, request_mock):
        # Update the response with list of permissions.
        request_mock.json = dtapiresponses.organization_permissions

        # Call the appropriate endpoint
        response = dt.Organization.list_permissions(
            organization_id='org_id',
        )

        # Assert output is of type list.
        assert type(response) == list

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.api_url+'/organizations/org_id/permissions'
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert only strings in output list.
        for permission in response:
            assert type(permission) == str
