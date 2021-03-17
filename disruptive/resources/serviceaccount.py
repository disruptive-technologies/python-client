from __future__ import annotations

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
        self.email = self.raw['email']
        self.display_name = self.raw['displayName']
        self.basic_auth = self.raw['enableBasicAuth']
        self.create_time = dttrans.iso8601_to_datetime(self.raw['createTime'])
        self.update_time = dttrans.iso8601_to_datetime(self.raw['updateTime'])

    @classmethod
    def get(cls,
            project_id: str,
            serviceaccount_id: str,
            auth: BasicAuth | OAuth | None = None
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
    def listing(cls,
                project_id: str,
                auth: BasicAuth | OAuth | None = None,
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
    def create(cls,
               project_id: str,
               display_name: str = '',
               basic_auth: bool = False,
               auth: BasicAuth | OAuth | None = None,
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
    def update(cls,
               project_id: str,
               serviceaccount_id: str,
               display_name: str = '',
               basic_auth: bool | None = None,
               auth: BasicAuth | OAuth | None = None,
               ):

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Construct body.
        body: dict = dict()
        if len(display_name) > 0:
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
    def delete(cls,
               project_id: str,
               serviceaccount_id: str,
               auth: BasicAuth | OAuth | None = None,
               ) -> None:

        # Construct URL.
        url = dt.base_url
        url += '/projects/{}/serviceaccounts/{}'.format(
            project_id,
            serviceaccount_id,
        )

        # Send DELETE request, but return nothing.
        dtrequests.delete(url=url)

    @classmethod
    def list_keys(cls,
                  project_id: str,
                  serviceaccount_id: str
                  ) -> list[Key]:
        pass


class Key(dtoutputs.OutputBase):

    def __init__(self, key: dict) -> None:
        # Inherit from Response parent.
        dtoutputs.OutputBase.__init__(self, key)

        # Initialize secret, which is only not-None when created.
        self.secret = None

        # Unpack organization json.
        self.__unpack()

    def __unpack(self) -> None:
        self.key_id = self.raw['id']
        self.create_time = self.raw['createTime']
        if 'secret' in self.raw:
            self.secret = self.raw['secret']
