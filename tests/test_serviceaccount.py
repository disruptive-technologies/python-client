# Project imports.
import disruptive as dt
import tests.mock_responses as dtresponses
import disruptive.transforms as dttrans


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
        assert s.basic_auth == res['enableBasicAuth']
        assert s.create_time == dttrans.iso8601_to_datetime(res['createTime'])
        assert s.update_time == dttrans.iso8601_to_datetime(res['updateTime'])

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

    def test_listing(self, request_mock):
        # Update the response data with list of serviceaccount data.
        request_mock.json = dtresponses.serviceaccounts

        # Call the appropriate endpoint
        sas = dt.ServiceAccount.listing('project_id')

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=dt.base_url+'/projects/project_id/serviceaccounts',
        )

        # Assert instances of Project in output list.
        for s in sas:
            assert isinstance(s, dt.ServiceAccount)

    def test_create(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = dt.ServiceAccount.create('project_id', 'new-sa', True)

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=dt.base_url+'/projects/project_id/serviceaccounts',
            body={'displayName': 'new-sa', 'enableBasicAuth': True},
        )

        # Assert attributes in output Device object.
        assert isinstance(s, dt.ServiceAccount)

    def test_update(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = dt.ServiceAccount.update(
            project_id='project_id',
            serviceaccount_id='serviceaccount_id',
            display_name='service-account-1',
            basic_auth=False,
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=dt.base_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
            body={'displayName': 'service-account-1', 'enableBasicAuth': False}
        )

        # Assert attributes in output Device object.
        assert isinstance(s, dt.ServiceAccount)

    def test_delete(self, request_mock):
        # Update the response status code to 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint.
        dt.ServiceAccount.delete(
            project_id='project_id',
            serviceaccount_id='serviceaccount_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=dt.base_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
        )
