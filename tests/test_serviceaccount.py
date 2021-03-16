# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses
import disruptive.transforms as dttransforms


class TestServiceAccount():

    def test_unpack(self, request_mock):
        # Update the response data with serviceaccount data.
        res = dtresponses.serviceaccount1
        request_mock.json = res

        # Call the appropriate endpoint.
        s = dt.ServiceAccount.get('project_id', 'serviceaccount_id')

        # Assert attributes unpacked correctly.
        assert s.email == res['email']
        assert s.display_name == res['displayName']
        assert s.basic_auth_enabled == res['enableBasicAuth']
        assert s.created == dttransforms.iso8601_to_datetime(res['createTime'])
        assert s.updated == dttransforms.iso8601_to_datetime(res['updateTime'])

    def test_get(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = dt.ServiceAccount.get('project_id', 'serviceaccount_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
        )

        # Assert attributes in output Device object.
        assert isinstance(s, dt.ServiceAccount)

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
