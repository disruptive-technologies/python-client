# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses


class TestServiceAccount():

    # def test_unpack(self, request_mock):
    #     # Update the response data with serviceaccount data.
    #     res = dtresponses.serviceaccount1
    #     request_mock.json = res

    #     # Call the appropriate endpoint.
    #     o = dt.ServiceAccount.get('organization_id')

    #     # Assert attributes unpacked correctly.
    #     assert o.display_name == res['displayName']
    #     assert o.organization_id == res['name'].split('/')[-1]

    def test_list(self, request_mock):
        # Update the response data with list of serviceaccount data.
        request_mock.json = dtresponses.serviceaccounts

        # Call the appropriate endpoint
        sas = dt.ServiceAccount.list('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/serviceaccounts',
        )

        # Assert instances of Project in output list.
        for s in sas:
            assert isinstance(s, dt.ServiceAccount)
