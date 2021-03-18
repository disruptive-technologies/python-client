# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestOrganization():

    def test_unpack(self, request_mock):
        # Update the response data with organization data.
        res = dtresponses.organization
        request_mock.json = res

        # Call the appropriate endpoint.
        o = dt.Organization.get('organization_id')

        # Assert attributes unpacked correctly.
        assert o.id == res['name'].split('/')[-1]
        assert o.display_name == res['displayName']

    def test_get(self, request_mock):
        # Update the response data with organization data.
        request_mock.json = dtresponses.organization

        # Call the appropriate endpoint.
        o = dt.Organization.get('organization_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/organizations/organization_id',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        assert isinstance(o, dt.Organization)

    def test_list(self, request_mock):
        # Update the response data with list of organization data.
        request_mock.json = dtresponses.organizations

        # Call the appropriate endpoint
        orgs = dt.Organization.list()

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/organizations',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for o in orgs:
            assert isinstance(o, dt.Organization)

    def test_list_members(self, request_mock):
        # Update the response data with list of organization data.
        request_mock.json = dtresponses.members

        # Call the appropriate endpoint
        members = dt.Organization.list_members('org_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/organizations/org_id/members',
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for m in members:
            assert isinstance(m, dt.outputs.Member)

    def test_add_member(self, request_mock):
        # Update the response data with list of organization data.
        request_mock.json = dtresponses.serviceaccount_member

        # Call the appropriate endpoint
        member = dt.Organization.add_member(
            organization_id='org_id',
            email='serviceaccount_email@domain.com',
            roles=['organization.administrator'],
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.base_url+'/organizations/org_id/members',
            body={
                'roles': ['roles/organization.administrator'],
                'email': 'serviceaccount_email@domain.com',
            }
        )

        # Assert single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        assert isinstance(member, dt.outputs.Member)
