from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive as dt
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
import disruptive.transforms as dttrans
from disruptive.authentication import BasicAuth, OAuth


class ServiceAccount(dtoutputs.OutputBase):

    def __init__(self, serviceaccount: dict) -> None:
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, serviceaccount)

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['name'].split('/')[-1]
        self.email = self.raw['email']
        self.display_name = self.raw['displayName']
        self.basic_auth = self.raw['enableBasicAuth']
        self.create_time = dttrans.iso8601_to_datetime(self.raw['createTime'])
        self.update_time = dttrans.iso8601_to_datetime(self.raw['updateTime'])

    @classmethod
    def get_serviceaccount(cls,
                           project_id: str,
                           serviceaccount_id: str,
                           auth: Optional[BasicAuth | OAuth] = None
                           ) -> ServiceAccount:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Return ServiceAccount object of GET request response.
        return cls(dtrequests.get(
            url=url,
            auth=auth
        ))

    @classmethod
    def list_serviceaccounts(cls,
                             project_id: str,
                             auth: Optional[BasicAuth | OAuth] = None,
                             ) -> list[ServiceAccount]:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts'.format(project_id)

        # Return list of ServiceAccount objects of paginated GET response.
        service_accounts = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='serviceAccounts',
            auth=auth,
        )
        return [cls(sa) for sa in service_accounts]

    @classmethod
    def create_serviceaccount(cls,
                              project_id: str,
                              display_name: str = '',
                              basic_auth: bool = False,
                              auth: Optional[BasicAuth | OAuth] = None,
                              ):

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts'.format(project_id)

        # Construct body.
        body: dict = dict()
        body['enableBasicAuth'] = basic_auth
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Return ServiceAccount object of GET request response.
        return (cls(dtrequests.post(
            url=url,
            body=body,
            auth=auth,
        )))

    @classmethod
    def update_serviceaccount(cls,
                              project_id: str,
                              serviceaccount_id: str,
                              display_name: Optional[str] = None,
                              basic_auth: Optional[bool] = None,
                              auth: Optional[BasicAuth | OAuth] = None,
                              ):

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Construct body.
        body: dict = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if basic_auth is not None:
            body['enableBasicAuth'] = basic_auth

        # Return ServiceAccount object of GET request response.
        return (cls(dtrequests.patch(
            url=url,
            body=body,
            auth=auth,
        )))

    @classmethod
    def delete_serviceaccount(cls,
                              project_id: str,
                              serviceaccount_id: str,
                              auth: Optional[BasicAuth | OAuth] = None,
                              ) -> None:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.delete(url=url)

    @staticmethod
    def get_key(project_id: str,
                serviceaccount_id: str,
                key_id: str,
                auth: Optional[BasicAuth | OAuth] = None,
                ) -> Key:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            serviceaccount_id,
            key_id,
        )

        # Return Key object of GET request response.
        return Key(dtrequests.get(
            url=url,
            auth=auth,
        ))

    @staticmethod
    def list_keys(project_id: str,
                  serviceaccount_id: str,
                  auth: Optional[BasicAuth | OAuth] = None,
                  ) -> list[Key]:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            serviceaccount_id,
        )

        # Return list of Key objects of paginated GET response.
        keys = dtrequests.auto_paginated_list(
            url=url,
            pagination_key='keys',
            auth=auth,
        )
        return [Key(key) for key in keys]

    @staticmethod
    def create_key(project_id: str,
                   serviceaccount_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> Key:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}/keys'.format(
            project_id,
            serviceaccount_id,
        )

        # Return Key object of POST request response.
        response = dtrequests.post(
            url=url,
            auth=auth,
        )
        return Key.with_secret(response)

    @staticmethod
    def delete_key(project_id: str,
                   serviceaccount_id: str,
                   key_id: str,
                   auth: Optional[BasicAuth | OAuth] = None,
                   ) -> None:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}/keys/{}'.format(
            project_id,
            serviceaccount_id,
            key_id,
        )

        # Return Key object of POST request response.
        dtrequests.delete(
            url=url,
            auth=auth,
        )


class Key(dtoutputs.OutputBase):

    def __init__(self, key: dict) -> None:
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, key)

        # Initialize secret, which is only not-None when created.
        self.secret = None

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.id = self.raw['id']
        self.create_time = dttrans.iso8601_to_datetime(self.raw['createTime'])
        if 'secret' in self.raw:
            self.secret = self.raw['secret']

    @classmethod
    def with_secret(cls, key: dict) -> Key:
        combined = key['key']
        combined['secret'] = key['secret']
        return cls(combined)
