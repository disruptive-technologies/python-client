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
        assert o.display_name == res['displayName']
        assert o.organization_id == res['name'].split('/')[-1]

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

        # Assert attributes in output Device object.
        assert isinstance(o, dt.Organization)

    def test_list(self, request_mock):
        # Update the response data with list of organization data.
        request_mock.json = dtresponses.organizations

        # Call the appropriate endpoint
        orgs = dt.Organization.get_list()

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/organizations',
        )

        # Assert instances of Project in output list.
        for o in orgs:
            assert isinstance(o, dt.Organization)
