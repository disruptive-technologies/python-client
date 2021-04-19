# Project imports.
import disruptive
import tests.api_responses as dtapiresponses
import disruptive.transforms as dttrans
from disruptive.resources.serviceaccount import Key


class TestServiceAccount():

    def test_repr(self, request_mock):
        # Update the response data with serviceaccount data.
        res = dtapiresponses.serviceaccount1
        request_mock.json = res

        # Fetch a serviceaccount.
        x = disruptive.ServiceAccount.get_serviceaccount(
            serviceaccount_id='serviceaccount_id',
            project_id='project_id',
        )

        # Evaluate __repr__ function and compare copy.
        y = eval(repr(x))
        assert x._raw == y._raw

    def test_unpack(self, request_mock):
        # Update the response data with serviceaccount data.
        res = dtapiresponses.serviceaccount1
        request_mock.json = res

        # Call the appropriate endpoint.
        s = disruptive.ServiceAccount.get_serviceaccount(
            'serviceaccount_id',
            'project_id',
        )

        # Assert attributes unpacked correctly.
        assert s.serviceaccount_id == res['name'].split('/')[-1]
        assert s.email == res['email']
        assert s.display_name == res['displayName']
        assert s.basic_auth == res['enableBasicAuth']
        assert s.create_time == dttrans.to_datetime(res['createTime'])
        assert s.update_time == dttrans.to_datetime(res['updateTime'])

    def test_get_serviceaccount(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = disruptive.ServiceAccount.get_serviceaccount(
            'serviceaccount_id',
            'project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        assert isinstance(s, disruptive.ServiceAccount)

    def test_list_serviceaccounts(self, request_mock):
        # Update the response data with list of serviceaccount data.
        request_mock.json = dtapiresponses.serviceaccounts

        # Call the appropriate endpoint
        sas = disruptive.ServiceAccount.list_serviceaccounts(
            'project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.api_url+'/projects/project_id/serviceaccounts',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert instances of Project in output list.
        for s in sas:
            assert isinstance(s, disruptive.ServiceAccount)

    def test_create_serviceaccount(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = disruptive.ServiceAccount.create_serviceaccount(
            'project_id',
            'new-sa',
            True,
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=disruptive.api_url+'/projects/project_id/serviceaccounts',
            body={'displayName': 'new-sa', 'enableBasicAuth': True},
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        assert isinstance(s, disruptive.ServiceAccount)

    def test_update_serviceaccount(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.serviceaccount1

        # Call the appropriate endpoint.
        s = disruptive.ServiceAccount.update_serviceaccount(
            serviceaccount_id='serviceaccount_id',
            project_id='project_id',
            display_name='service-account-1',
            basic_auth=False,
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Verify request parameters.
        request_mock.assert_requested(
            method='PATCH',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
            body={'displayName': 'service-account-1', 'enableBasicAuth': False}
        )

        # Assert attributes in output Device object.
        assert isinstance(s, disruptive.ServiceAccount)

    def test_delete_serviceaccount(self, request_mock):
        # Update the response status code to 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint.
        disruptive.ServiceAccount.delete_serviceaccount(
            serviceaccount_id='serviceaccount_id',
            project_id='project_id',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id',
        )

    def test_key_attributes(self, request_mock):
        # Update the response data with serviceaccount data.
        res = dtapiresponses.key_without_secret
        request_mock.json = res

        # Call the appropriate endpoint.
        k = disruptive.ServiceAccount.get_key(
            'serviceaccount_id',
            'key_id',
            'project_id',
        )

        # Assert attributes unpacked correctly.
        assert k.key_id == res['name'].split('/')[-1]
        assert k.create_time == dttrans.to_datetime(res['createTime'])
        assert k.secret is None

    def test_key_secret_set(self, request_mock):
        # Update the response data with serviceaccount data.
        res = dtapiresponses.key_with_secret
        request_mock.json = res

        # Call the appropriate endpoint.
        k = disruptive.ServiceAccount.create_key(
            'serviceaccount_id',
            'project_id',
        )

        # Assert attributes unpacked correctly.
        assert k.secret == res['secret']

    def test_get_key(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.key_without_secret

        # Call the appropriate endpoint.
        key = disruptive.ServiceAccount.get_key(
            serviceaccount_id='serviceaccount_id',
            key_id='key_id',
            project_id='project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id/keys/key_id',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        assert isinstance(key, Key)

    def test_list_keys(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.keys

        # Call the appropriate endpoint.
        keys = disruptive.ServiceAccount.list_keys(
            serviceaccount_id='serviceaccount_id',
            project_id='project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='GET',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id/keys',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        for key in keys:
            assert isinstance(key, Key)

    def test_create_key(self, request_mock):
        # Update the response data with serviceaccount data.
        request_mock.json = dtapiresponses.key_with_secret

        # Call the appropriate endpoint.
        key = disruptive.ServiceAccount.create_key(
            serviceaccount_id='serviceaccount_id',
            project_id='project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='POST',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id/keys',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)

        # Assert attributes in output Device object.
        assert isinstance(key, Key)

    def test_delete_key(self, request_mock):
        # Update the response status code to 200.
        request_mock.status_code = 200

        # Call the appropriate endpoint.
        disruptive.ServiceAccount.delete_key(
            serviceaccount_id='serviceaccount_id',
            key_id='key_id',
            project_id='project_id',
        )

        # Verify request parameters.
        request_mock.assert_requested(
            method='DELETE',
            url=disruptive.api_url+'/projects/project_id/'
            + 'serviceaccounts/serviceaccount_id/keys/key_id',
        )

        # Verify single request sent.
        request_mock.assert_request_count(1)
